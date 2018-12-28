""" tests on the artillary class """
from .. import artillary

def test_defaults():
    """ ensure the default color is red """
    gun = artillary.Gun((0, 0))
    assert gun.color == (250, 90, 90)
    assert gun.size == 20
    assert gun.position == (0, 0)

def test_shell():
    """ ensure the default color is red """
    init_velocity = (2, 3)
    init_position = (15, 17)
    shell = artillary.Shell(init_position, init_velocity)
    #assert shell.color == (0, 0, 0)
    assert shell.size == 3
    assert shell.position == init_position
    assert shell.velocity == init_velocity

# def test_blob_params():
#     """ tests that the named parameters work as expected """
#     position = (50, 12)
#     color = (128, 255, 54)
#     size = 55
#
#     blob = blobs.Blob(position=position, color=color, size=size)
#     assert blob.color == color
#     assert blob.position == position
#     assert blob.size == size
#
def test_shell_move():
    """ tests the some basic movement rules """
    shell = artillary.Shell(position=(25, 34), velocity=(13, 12))
    shell.move()
    assert shell.position == (38, 46)

# def test_blob_move_walls():
#     """
#     tests boundary (0 side)
#
#     """
#     blob = blobs.Blob(position=(10, 25), velocity=(-20, -15), size=5)
#     # one move will hit the x 0-wall boundary  (-10, 10) will 'bounce' to (5,10)
#     blob.move()
#     assert blob.position == (5, 10)
#     assert blob.velocity == (20, -15)
#
#     # next move should put us at -15,-5; bounch to 5,5
#     blob.move()
#     assert blob.position == (25, 5)
#     assert blob.velocity == (20, 15)
#
#     # next move should put us at -15,-5; bounch to 5,5
#     blob.move()
#     assert blob.position == (45, 20)
#     assert blob.velocity == (20, 15)
#
#
#
# def test_blob_distance():
#     """
#     tests the force calculation of a blob
#     """
#     blob = blobs.Blob(position=(10, 10), size=5)
#     assert blob.distance((20, 10)) == 10
#
#     # test a diagonal
#     assert blob.distance((13, 14)) == 5
#     assert blob.distance((40, 50)) == 50 #sqrt (900 + 1600) = sqrt(2500)= 50
#
#     # go the other directions
#     assert blob.distance((20, 10)) == 10
#     assert blob.distance((10, 3)) == 7
#     assert blob.distance((10, 55)) == 45
#
#
# def test_blob_forces():
#     """
#     tests the force calculation of a blob
#     """
#
#     # distance is 10;
#     #  magnitude should be 5**2 / 10**2 = (1/2)**2 = 1/4
#     #  direction is (1,0)
#     blob = blobs.Blob(position=(10, 10), size=5)
#     blob2 = blobs.Blob(position=(20, 10), size=5)
#     blob3 = blobs.Blob(position=(0, 10), size=5)
#     blob4 = blobs.Blob(position=(10, 20), size=5)
#     blob2blue = blobs.Blob(position=(20, 10), size=5, color=(0, 0, 255))
#     blob3blue = blobs.Blob(position=(0, 10), size=5, color=(0, 0, 255))
#     blob4blue = blobs.Blob(position=(10, 20), size=5, color=(0, 0, 255))
#
#     force = blob.calc_forces([blob2])
#     assert force == (-0.25, 0.0)
#
#     force = blob.calc_forces([blob4])
#     assert force == (0.0, -0.25)
#
#
#     force = blob.calc_forces([blob2blue])
#     assert force == (0.25, 0.0)
#
#
#     force = blob.calc_forces([blob3])
#     assert force == (0.25, 0.0)
#
#     force = blob.calc_forces([blob2, blob3])
#     assert force == (0.0, 0.0)
#
#
#
# def test_add_vectors():
#     v1 = (1, 2, 3)
#     v2 = (5, 2, 7)
#     assert blobs.add_tuple(v1, v2) == (6, 4, 10)
