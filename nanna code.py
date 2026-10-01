import pygame
import sys

# Define the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Initialize Pygame
pygame.init()
pygame.font.init()


class Checkbox:
    def __init__(self, surface, x, y, idnum, prices, color=(230, 230, 230),
                 caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0),
                 font_size=22, font_color=(0, 0, 0),
                 text_offset=(28, 1), font='Ariel Black'):
        self.surface = surface
        self.x = x
        self.y = y
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = font_size
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        # identification for removal and reorganization
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12, 12)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

        # total keeps track of the total price
        self.prices = prices
        self.total = 0

    def _draw_button_text(self):
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 +
                         self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6, self.y + 6), 4)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
                self.total -= self.prices.get(self.idnum + 1, 0)  # subtract prices if unchecked
            else:
                self.checked = True
                self.total += self.prices.get(self.idnum + 1, 0)  # add price if it's checked

    def update_checkbox(self, event_object):
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)


def create_checkboxes(surface, prices):
    buttons = []
    button_positions = [
        (50, 200, 'Pepperoni $1.50'),
        (50, 225, 'Mushrooms $1.00'),
        (50, 250, 'Onions $2.50'),
        (50, 275, 'Bell Peppers $1.50'),
        (50, 300, 'Olives $1.50'),
        (50, 325, 'Basil $0.50'),
        (50, 350, 'Oregano $0.25'),
        (50, 375, 'Garlic $3.00')
    ]

    for i, (x, y, caption) in enumerate(button_positions):
        button = Checkbox(surface, x, y, i, prices, caption=caption)
        buttons.append(button)

    return buttons


def draw_total_price(screen, total):
    font = pygame.font.SysFont('Arial', 25)
    font.set_bold(True)
    pygame.draw.rect(screen, "red", (50, 425, 165, 50))
    text_surface = font.render('Total : $' + str(total), True, 'Black')
    screen.blit(text_surface, (70, 435))


def draw_checkbox_images(screen, circleX, circleY, radius, radius2, button_list):
    for button in button_list:
        if button.checked:
            image = pygame.image.load(button.caption.split()[0] + ".png")
            image = pygame.transform.scale(image, (50, 50))
            screen.blit(image, (circleX - 50, circleY - 50))

    pygame.draw.circle(screen, ("Khaki1"), (circleX, circleY), radius)
    pygame.draw.circle(screen, ('Red'), (circleX, circleY), radius2)


def main():
    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create two surfaces to split the frame
    surface1 = pygame.Surface((SCREEN_WIDTH * 0.3, SCREEN_HEIGHT))
    surface2 = pygame.Surface((SCREEN_WIDTH * 0.7, SCREEN_HEIGHT))

    # Fill the surfaces with different colors
    surface1.fill((255, 255, 255))
    surface2.fill((0, 200, 0))

    # Blit the surfaces to the screen
    screen.blit(surface1, (0, 0))
    screen.blit(surface2, (SCREEN_WIDTH * 0.3, 0))

    Prices = {1: 1.5, 2: 1, 3: 2.5, 4: 1.5, 5: 1.5, 6: 0.5, 7: 0.25, 8: 3}
    boxes = create_checkboxes(screen, Prices)

    circleX = 500
    circleY = 300
    radius = 150
    radius2 = 130

    baseprice = 10.00

    # Run the game loop
    while True:

        # Check for events
        for event in pygame.event.get():
            # If the user clicks the any of the checkboxes, highlight that checkbox
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in boxes:
                    box.update_checkbox(event)

            # If the user clicks the close button, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate total price
        total = baseprice
        for box in boxes:
            total += box.total

        # Draw the frame
        screen.fill((0, 0, 0))
        screen.blit(surface1, (0, 0))
        screen.blit(surface2, (SCREEN_WIDTH * 0.3, 0))

        for box in boxes:
            box.render_checkbox()

        draw_checkbox_images(screen, circleX, circleY, radius, radius2, boxes)

        draw_total_price(screen, total)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()