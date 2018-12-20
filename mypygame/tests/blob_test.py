""" tests on the blob class """
from .. import blobs

def test_defaults():
    """ ensure the default color is red """
    blob = blobs.Blob()
    assert blob.color == (255, 0, 0)
    assert blob.size == 10
    assert blob.position == (0, 0)

def test_blob_params():
    """ tests that the named parameters work as expected """
    position = (50, 12)
    color = (128, 255, 54)
    size = 55

    blob = blobs.Blob(position=position, color=color, size=size)
    assert blob.color == color
    assert blob.position == position
    assert blob.size == size

def test_blob_move():
    """ tests the some basic movement rules """
    blob = blobs.Blob(position=(10, 10))
