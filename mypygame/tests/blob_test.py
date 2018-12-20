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
    blob = blobs.Blob(position=(25, 34), velocity=(13, 12))
    blob.move()
    assert blob.position == (38, 46)

def test_blob_move_walls():
    """
    tests boundary (0 side)

    """
    blob = blobs.Blob(position=(10, 25), velocity=(-20, -15), size=5)
    # one move will hit the x 0-wall boundary  (-10, 10) will 'bounce' to (5,10)
    blob.move()
    assert blob.position == (5, 10)
    assert blob.velocity == (20, -15)

    # next move should put us at -15,-5; bounch to 5,5
    blob.move()
    assert blob.position == (25, 5)
    assert blob.velocity == (20, 15)

    # next move should put us at -15,-5; bounch to 5,5
    blob.move()
    assert blob.position == (45, 20)
    assert blob.velocity == (20, 15)



def test_blob_forces():
    """
    tests the force calculation of a blob
    """
    blob = blobs.Blob(position=(10, 10), size=5)
    blob2 = blobs.Blob(position=(20, 10), size=5)
    distance = blob.distance(blob2.position)
    assert distance is not None
