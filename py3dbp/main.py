from .constants import RotationType, Axis
from .auxiliary_methods import intersect, set_to_decimal

DEFAULT_NUMBER_OF_DECIMALS = 3
START_POSITION = [0, 0, 0]


class Item:
    def __init__(self, name, width, height, depth, rotate):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.rotate = rotate
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS

    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        else:
            dimension = []

        return dimension


class Bin:
    def __init__(self, name, width, height, depth):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.items = []
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS

    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )

    def put_item(self, item, pivot):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        for i in range(0, len(RotationType.ALL) if item.rotate else 1):
            item.rotation_type = i
            dimension = item.get_dimension()
            if (
                self.width < pivot[0] + dimension[0] or
                self.height < pivot[1] + dimension[1] or
                self.depth < pivot[2] + dimension[2]
            ):
                continue

            fit = True

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                self.items.append(item)

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit


def pack_to_bin(bin, item):
    fitted = False

    if not bin.items:
        response = bin.put_item(item, START_POSITION)
        if not response:
            bin.unfitted_items.append(item)
        return True

    for axis in range(0, 3):
        items_in_bin = bin.items
        for ib in items_in_bin:
            pivot = [0, 0, 0]
            w, h, d = ib.get_dimension()
            if ib.rotate:
                if axis == Axis.WIDTH:
                    pivot = [
                        ib.position[0] + w,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.HEIGHT:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + h,
                        ib.position[2]
                    ]
                elif axis == Axis.DEPTH:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + d
                    ]
            if bin.put_item(item, pivot):
                fitted = True
                break
        if fitted:
            break
    return fitted


def pack(binx, biny, binz, items, return_bins=False, number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS):
    bin = Bin("", binx, binz, biny)
    bin.format_numbers(number_of_decimals)
    bins = [bin]
    bins_idxs = []

    for item in items:
        item.format_numbers(number_of_decimals)

    item_idx = 0
    for bin in bins:
        items_in_bin = []
        for i in range(item_idx, len(items)):
            fitted = pack_to_bin(bin, items[i])
            if not fitted:
                bins.append(Bin("", bins[0].width, bins[0].height, bins[0].depth))
                break
            items_in_bin.append(items[i].name)
            item_idx += 1
        bins_idxs.append(items_in_bin)

    return bins if return_bins else bins_idxs

