class OverlayManager:
    def __init__(self):
        self.overlay = {}
        self.overlay_current = None
        self.overlay_active = False

    def update(self):
        if self.overlay_current != None:
            self.overlay[self.overlay_current].update()

    def draw(self):
        if self.overlay_current != None:
            self.overlay[self.overlay_current].draw()

    def register_overlay(self, overlay):
        overlay_name = overlay.OVERLAY_NAME
        self.overlay[overlay_name] = overlay

    def load_overlay(self, overlay_name):
        self.overlay_current = overlay_name
        self.overlay_active = True

    def unload_overlay(self):
        self.overlay_current = None
        self.overlay_active = False
        
OVERLAY_MANAGER = OverlayManager()