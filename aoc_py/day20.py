import attr
import numpy as np
from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG

grammar = r'''
    document = particle+ EOF
    particle = pos sep vel sep acc
    pos = "p" open int sep int sep int close
    vel = "v" open int sep int sep int close
    acc = "a" open int sep int sep int close
    open = "=<"
    close = ">"
    sep = ","
    int = "-"? digit+
    digit = r'[0-9]'
'''

parser = ParserPEG(grammar, root_rule_name='document', debug=False, skipws=True)


class ParticleVisitor(PTNodeVisitor):
    def visit_document(self, node, children):
        return children

    def visit_particle(self, node, children):
        pos, vel, acc = children
        return Particle(pos, vel, acc)

    def visit_pos(self, node, children):
        return np.array(list(children))

    def visit_vel(self, node, children):
        return np.array(list(children))

    def visit_acc(self, node, children):
        return np.array(list(children))

    def visit_int(self, node, children):
        return int(''.join(children))


@attr.s
class Particle:
    pos = attr.ib()
    vel = attr.ib()
    acc = attr.ib()


def parse_particles(particles):
    parse_tree = parser.parse(particles)
    return visit_parse_tree(parse_tree, ParticleVisitor())


def closest_particle(particles):
    positions = np.array([p.pos for p in particles])
    velocities = np.array([p.vel for p in particles])
    accelerations = np.array([p.acc for p in particles])

    # Once `closest` has been the same for `limit` ticks, consider it converged.
    ticks_equal = 0
    closest = None
    limit = 100000

    while True:
        velocities += accelerations
        positions += velocities
        distances = np.sum(np.abs(positions), axis=1)

        cur_closest = np.argmin(distances)
        if cur_closest != closest:
            ticks_equal = 0
            closest = cur_closest
        else:
            ticks_equal += 1

        if ticks_equal >= limit:
            print(f'Part 1: particle {cur_closest} is closest.')
            break


def collisions(particles):
    positions = np.array([p.pos for p in particles])
    velocities = np.array([p.vel for p in particles])
    accelerations = np.array([p.acc for p in particles])

    ticks_equal = 0
    limit = 100000
    num_particles = None

    while True:
        velocities += accelerations
        positions += velocities

        values, counts = np.unique(positions, return_counts=True, axis=0)
        collisions = values[counts > 1]

        # Couldn't figure out how to vectorize this, so do it for each collision
        for pos in collisions:
            # Construct a mask of which values to delete
            mask = np.ones(len(positions), dtype=bool)
            del_mask, = np.where((positions == pos).all(axis=1))
            mask[del_mask] = False

            # Remove collisions
            positions = positions[mask]
            velocities = velocities[mask]
            accelerations = accelerations[mask]

        cur_num = len(positions)

        if cur_num != num_particles:
            ticks_equal = 0
            num_particles = cur_num
        else:
            ticks_equal += 1

        if ticks_equal >= limit:
            print(f'Part 2: {cur_num} particles remaining.')
            break


if __name__ == '__main__':
    with open('../input/20.txt') as fp:
        particles = parse_particles(fp.read().strip())

    closest_particle(particles)
    collisions(particles)
