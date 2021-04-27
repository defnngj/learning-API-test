import pytest


def colors():
    colors_list = []
    for i in range(10):
        colors_list.append("red"+str(i))
    return colors_list


@pytest.mark.parametrize('color', colors())
def test_colors(color):
    assert color != 'mauve'
