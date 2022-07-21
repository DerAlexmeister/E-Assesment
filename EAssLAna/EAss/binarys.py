

def get_super(x):
    ## Link: https://www.geeksforgeeks.org/how-to-print-superscript-and-subscript-in-python/
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)


def getBinaryCalcList(a):
    binary_parts = []
    try:
        for i, e in enumerate(reversed(a)):
            binary_parts.append("({} x 2{})".format(e, get_super(str(i))))
        binary_parts = list(reversed(binary_parts))
    except Exception as error:
        print(error)
    return binary_parts
