from . import prepare,tools
from .states import title_screen, viewing, gallery_screen

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "VIEWING": viewing.Viewing(),
                   "GALLERY": gallery_screen.GalleryScreen()}
    controller.setup_states(states, "TITLE")
    controller.main()
