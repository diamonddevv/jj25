from __future__ import annotations
import pygame

from src.render import spritesheet

class PixelFont():
    GLYPHXEL: PixelFont | None = None

    def __init__(self, 
                 name: str, 
                 spritesheet: spritesheet.Spritesheet, 
                 rows: int, columns: int, 
                 codepoints: str, *,
                 caps_only: bool = False, general_glyph_width_override: int = 0, specific_character_widths: dict[str, int] = {}
                 ):
        self.name = name
        self.spritesheet = spritesheet
        self.codepoints = codepoints
        self.caps_only = caps_only

        self.glyph_width = spritesheet.cell_w if general_glyph_width_override <= 0 else general_glyph_width_override
        self.specific_character_widths = specific_character_widths

        self.rows = rows
        self.cols = columns 

    
    def get_character_width(self, char: str) -> int:
        if char in self.specific_character_widths:
            return self.specific_character_widths[char]
        else:
            return self.glyph_width

    def get_codepoint_pos(self, char: str) -> tuple[int, int]:
        if self.caps_only:
            char = char.upper()

        if len(char) != 1:
            raise ValueError("char must be a single character")
        
        if not char in self.codepoints:
            raise ValueError(f"char must be in the list of codepoints, {char} is not")
        
        idx = self.codepoints.index(char)
        x = 0
        y = 0

        while idx >= self.cols:
            y += 1
            idx -= self.cols
        x = idx

        return (x, y)


    def verify_all_codepoints(self, text: str) -> bool:
        for c in text:
            if not c in self.codepoints and not c in ['\x0a']: # ignore line feeds
                return False
        return True

    def calculate_size_for_text(self, text: str) -> tuple[int, int]:
        longest_line_width = -1
        lines = 1

        line_width = 0

        for char in text:
            if char == '\n':
                lines += 1
                if line_width > longest_line_width:
                    longest_line_width = line_width
                line_width = 0
            else:
                line_width += self.get_character_width(char)

        if line_width > longest_line_width:
            longest_line_width = line_width

        return (longest_line_width, lines * self.spritesheet.cell_h)

    def render(self, text: str) -> pygame.Surface:
        if self.caps_only:
            text = text.upper()

        size = self.calculate_size_for_text(text)
        surface = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)

        width_pos = 0
        line = 0
        for char in text:

            if char == '\n':
                line += 1
                width_pos = 0
            else:
                pos = self.get_codepoint_pos(char)
                width = self.get_character_width(char)
                self.spritesheet.fast_cell_blit_to_surface(pos[0], pos[1], surface, (width_pos, line * self.spritesheet.cell_h))
                width_pos += width

        return surface

    @staticmethod
    def init_pixelfonts():
        PixelFont.GLYPHXEL = PixelFont("Glyphxel", Spritesheet(data.load_texture("font/glyphxel.png"), 0, 0, 16, 16), 16, 16,
                                    "ABCDEFGHIJKLMNOP" +
                                    "QRSTUVWXYZ ,.!?|" +
                                    "abcdefghijklmnop" +
                                    "qrstuvwxyz£¢$€\"'"+
                                    "0123456789=-+*/\\"+
                                    "ÄÅÖÕÜŽŠẞ        " +
                                    "äåöõüžšß        " +
                                    "()<>[]{}:;^%&_  "
                                    , caps_only=False, general_glyph_width_override=8,
                                    specific_character_widths={
                                        'a': 7,
                                        'i': 5,
                                        'l': 6,
                                        '.': 4,
                                        ',': 4,
                                        "'": 4,
                                    })

    @staticmethod
    def glyphxel() -> PixelFont:
        if not PixelFont.GLYPHXEL:
            PixelFont.init_pixelfonts()
        assert PixelFont.GLYPHXEL
        return PixelFont.GLYPHXEL
    
