import numpy as np
import pytest

from foolbox.attacks import BoundaryAttack
from foolbox.attacks import DeepFoolAttack
from foolbox.attacks import BlendedUniformNoiseAttack


# Filter warnings because of this issue:
# https://github.com/bashtage/randomgen/issues/11


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack(bn_adversarial):
    adv = bn_adversarial
    attack = BoundaryAttack()
    attack(adv, iterations=200, verbose=True)
    assert adv.image is not None
    assert adv.distance.value < np.inf


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_non_verbose(bn_adversarial):
    adv = bn_adversarial
    attack = BoundaryAttack()
    attack(adv, iterations=200, verbose=False)
    assert adv.image is not None
    assert adv.distance.value < np.inf


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_continue(bn_adversarial):
    adv = bn_adversarial
    attack1 = BlendedUniformNoiseAttack()
    attack1(adv)
    d1 = adv.distance.value
    attack2 = BoundaryAttack()
    attack2(adv, iterations=200, verbose=True)
    assert adv.image is not None
    assert adv.distance.value < np.inf
    assert adv.distance.value < d1


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_parameters(bn_adversarial):
    adv = bn_adversarial
    attack = BoundaryAttack()
    o = adv.original_image
    np.random.seed(2)
    starting_point = np.random.uniform(
        0, 1, size=o.shape).astype(o.dtype)
    attack(
        adv,
        iterations=200,
        starting_point=starting_point,
        log_every_n_steps=2,
        tune_batch_size=False,
        threaded_rnd=False,
        threaded_gen=False,
        alternative_generator=True,
        verbose=True)
    assert adv.image is not None
    assert adv.distance.value < np.inf


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_parameters2(bn_adversarial):
    adv = bn_adversarial
    attack = BoundaryAttack()
    attack(
        adv,
        iterations=200,
        alternative_generator=True,
        verbose=True)
    assert adv.image is not None
    assert adv.distance.value < np.inf


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_parameters3(bn_adversarial):
    adv = bn_adversarial
    attack = BoundaryAttack()
    o = adv.original_image
    np.random.seed(2)
    starting_point = np.random.uniform(
        0, 1, size=o.shape).astype(o.dtype)
    attack(
        adv,
        iterations=200,
        starting_point=starting_point,
        log_every_n_steps=2,
        tune_batch_size=30,
        threaded_rnd=False,
        threaded_gen=False,
        verbose=True)
    assert adv.image is not None
    assert adv.distance.value < np.inf


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_gl(gl_bn_adversarial):
    adv = gl_bn_adversarial
    attack = BoundaryAttack()
    attack(adv, iterations=200, verbose=True)
    assert adv.image is not None
    assert adv.distance.value < np.inf


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_impossible(bn_impossible):
    adv = bn_impossible
    attack = BoundaryAttack()
    attack(adv, iterations=200, verbose=True)
    assert adv.image is None
    assert adv.distance.value == np.inf


@pytest.mark.filterwarnings("ignore:can't resolve package")
def test_attack_convergence(bn_adversarial):
    adv = bn_adversarial
    attack1 = DeepFoolAttack()
    attack1(adv)
    attack2 = BoundaryAttack()
    attack2(adv, iterations=5000, verbose=True)
    # should converge
    assert adv.image is not None
    assert adv.distance.value < np.inf
