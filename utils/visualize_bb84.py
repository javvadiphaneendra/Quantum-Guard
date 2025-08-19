import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_bb84(alice_bits, bob_bits=None, interval=300, save=False, filename="bb84_animation.gif"):
    """
    Animate BB84 bits transmission.
    alice_bits : list of 0/1 sent by Alice
    bob_bits : optional, list of 0/1 received by Bob
    """
    n = len(alice_bits)
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.set_xlim(-1, n)
    ax.set_ylim(-1, 2)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['0', '1'])
    ax.set_xlabel("Bit position")
    ax.set_title("BB84 Key Transmission Animation")
    alice_dots, = ax.plot([], [], 'ro', label="Alice")
    bob_dots, = ax.plot([], [], 'bo', label="Bob")
    ax.legend()

    def init():
        alice_dots.set_data([], [])
        bob_dots.set_data([], [])
        return alice_dots, bob_dots

    def update(frame):
        alice_x = list(range(frame+1))
        alice_y = alice_bits[:frame+1]
        alice_dots.set_data(alice_x, alice_y)
        if bob_bits:
            bob_x = list(range(frame+1))
            bob_y = bob_bits[:frame+1]
            bob_dots.set_data(bob_x, bob_y)
        return alice_dots, bob_dots

    ani = animation.FuncAnimation(fig, update, frames=n, init_func=init, blit=True, interval=interval, repeat=False)

    if save:
        ani.save(filename, writer='pillow')
    plt.show()
