from __future__ import annotations

import random

import embed_templator


class Embed(embed_templator.Embed):

    def setup(self) -> Embed:
        lucky: str = (
            "There was 1 / 1 000 000 chance for this message to show 🍀"
        ) * (not random.randint(0, 1_000_000))

        self.set_footer(
            icon_url=self.client.user.avatar_url,
            text=lucky or '   '.join(
                (
                    f"⚙️ {self.ctx.time() * 1000:.2f} ms",
                    f"⏳ {self.client.latency * 1000:.2f}ms",
                    f"🔑 {self.ctx.prefix}help",
                )
            )
        )

        return self.set_author(
            name=f"Requested by {self.ctx.author} 🚀",
            icon_url=self.ctx.author.avatar_url
        )
