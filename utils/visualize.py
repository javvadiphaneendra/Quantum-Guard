import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_bb84(qber, save=False):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    titles = ["Clean Channel", "With Eve"]

    # Setup both subplots
    for ax, title in zip(axes, titles):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_title(title, fontsize=14)

    # Clean channel objects
    alice_clean = axes[0].text(0.1, 0.5, "Alice", fontsize=12, ha="center",
                               bbox=dict(boxstyle="round", facecolor="lightblue"))
    bob_clean = axes[0].text(0.9, 0.5, "Bob", fontsize=12, ha="center",
                             bbox=dict(boxstyle="round", facecolor="lightgreen"))
    msg_clean, = axes[0].plot([], [], "o-", color="blue", lw=2)

    # With Eve objects
    alice_eve = axes[1].text(0.1, 0.7, "Alice", fontsize=12, ha="center",
                             bbox=dict(boxstyle="round", facecolor="lightblue"))
    bob_eve = axes[1].text(0.9, 0.7, "Bob", fontsize=12, ha="center",
                           bbox=dict(boxstyle="round", facecolor="lightgreen"))
    eve = axes[1].text(0.5, 0.3, "Eve", fontsize=12, ha="center",
                       bbox=dict(boxstyle="round", facecolor="salmon"))
    msg_eve1, = axes[1].plot([], [], "o--", color="red", lw=2)
    msg_eve2, = axes[1].plot([], [], "o--", color="red", lw=2)

    # QBER text
    qber_text = axes[1].text(0.5, 0.9, f"QBER ~ {qber*100:.1f}%",
                             fontsize=10, ha="center")

    def init():
        msg_clean.set_data([], [])
        msg_eve1.set_data([], [])
        msg_eve2.set_data([], [])
        return msg_clean, msg_eve1, msg_eve2

    def update(frame):
        # Clean channel movement (Alice -> Bob)
        x_clean = [0.2 + 0.6 * (frame / 100), 0.2 + 0.6 * (frame / 100)]
        y_clean = [0.5, 0.5]
        msg_clean.set_data(x_clean, y_clean)

        # With Eve movement (Alice -> Eve -> Bob)
        if frame <= 50:
            # Alice -> Eve
            x_eve1 = [0.2 + 0.3 * (frame / 50), 0.2 + 0.3 * (frame / 50)]
            y_eve1 = [0.7 - 0.4 * (frame / 50), 0.7 - 0.4 * (frame / 50)]
            msg_eve1.set_data(x_eve1, y_eve1)
            msg_eve2.set_data([], [])
        else:
            # Eve -> Bob
            f = (frame - 50) / 50
            x_eve2 = [0.5 + 0.4 * f, 0.5 + 0.4 * f]
            y_eve2 = [0.3 + 0.4 * f, 0.3 + 0.4 * f]
            msg_eve2.set_data(x_eve2, y_eve2)

        return msg_clean, msg_eve1, msg_eve2

    ani = animation.FuncAnimation(fig, update, frames=100, init_func=init,
                                  blit=True, interval=50, repeat=True)

    if save:
        ani.save("keys/bb84_animation.gif", writer="pillow", fps=20)
        print("✅ Animation saved at keys/bb84_animation.gif")

    plt.show()
