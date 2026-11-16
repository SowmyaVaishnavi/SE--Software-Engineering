"""
collisions: puck-vs-paddle collision handling.
"""

def handle_paddle_collision(puck, paddle):
    """
    If the puck overlaps the paddle, bounce it off.
    Returns True if a collision was handled this frame.
    """
    dx = puck.x - paddle.x
    dy = puck.y - paddle.y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    if distance < puck.radius + paddle.radius:
        # Avoid division by zero if the centers overlap exactly.
        if distance == 0:
            dx = 1
            dy = 0
            distance = 1

        # Collision normal from paddle to puck.
        nx = dx / distance
        ny = dy / distance

        # Reflect puck velocity around the collision normal.
        dot = puck.vx * nx + puck.vy * ny
        puck.vx = puck.vx - 2 * dot * nx
        puck.vy = puck.vy - 2 * dot * ny

        # Move the puck outside the paddle to prevent repeated overlap.
        overlap = puck.radius + paddle.radius - distance
        puck.x += nx * overlap
        puck.y += ny * overlap

        return True

    return False