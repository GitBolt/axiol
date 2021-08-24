import embed_templator


class Embed(embed_templator.Embed):

    def setup(self):
        self.set_footer(text="Hello World!")
        return self
