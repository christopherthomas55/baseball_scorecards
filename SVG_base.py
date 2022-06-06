import config



# Inconsistent with kwargs vs dicts
class SVGElement:
    def __init__(self, name, **kwargs):
        self.attributes = kwargs
        self.name = name
        pass

    def add_atrributes(self, **kwargs):
        for attr, val in kwargs.items():
            assert(isinstance(attr, str))
            assert(isinstance(val, str))
            self.attributes[attr] = val

    def add_attribute_dict(self, attri_dict):
        for attr, val in attri_dict.items():
            self.attributes[attr] = val

    def get_xml(self):
        assert(self.name)
        out = ' '.join(['{attr}="{val}"'.format(attr=attr, val=val) for attr, val in self.attributes.items()])
        return "<{name} {out} />\n".format(name=self.name, out=out)

# TODO - add grouping functionality
class SVGBase:
    def __init__(self, height=config.DEFAULT_HEIGHT, width=config.DEFAULT_WIDTH):
        self.width = width
        self.height = height
        self.children = []
        self.add_rect({"fill":"white", "width":self.width, "height":self.height, "stroke":"black", "x":"0", "y":"0"})

    # Gotta be a clever way to simplify below adds
    def add_rect(self, attributes):
        must_have = ["fill", "stroke", "x", "y", "width", "height"]
        assert(all([x in attributes for x in must_have]))
        temp = SVGElement("rect")
        temp.add_attribute_dict(attributes)
        self.children.append(temp)

    def add_line(self, attributes):
        must_have = ["x1", "y1", "x2", "y2", "stroke", "stroke-width"]
        assert(all([x in attributes for x in must_have]))
        temp = SVGElement("line")
        temp.add_attribute_dict(attributes)
        self.children.append(temp)

    def add_polyline(self, attributes):
        must_have = ["points", "fill", "stroke"]
        assert(all([x in attributes for x in must_have]))
        temp = SVGElement("polyline")
        temp.add_attribute_dict(attributes)
        self.children.append(temp)

    def add_circle(self):
        pass

    def add_semicircle(self):
        pass

    def add_text(self, text):
        # Yes....not handling quotes well yet
        assert("'" not in text)

    def add_custom(self, name, attributes):
        pass

    def reset(self):
        self.children = []
        self.add_rect({"fill":"white", "width":self.width, "height":self.height, "stroke":"black", "x":"0", "y":"0"})

    def save(self, filename):
        assert(filename.endswith('.svg'))

        with open(filename, "w") as f:
            f.write(config.BASE_HEADER.format(height=self.height, width=self.width))

            for c in self.children:
                f.write(c.get_xml())

            # Simple closer for now
            f.write("</svg>")


if __name__ == "__main__":
    test = SVGBase()
    test.save("test.svg")
