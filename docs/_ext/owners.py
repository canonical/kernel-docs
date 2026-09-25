from docutils.parsers.rst import Directive

class OwnersDirective(Directive):
    required_arguments = 1
    final_argument_whitespace = True  # allow spaces inside argument
    has_content = False

    def run(self):
        raw = self.arguments[0]

        # Split on commas, allow spaces in each item
        owners = [o.strip() for o in raw.split(",") if o.strip()]

        env = self.state.document.settings.env

        # Store globally (optional, useful for post-processing)
        if not hasattr(env, "owners_all"):
            env.owners_all = []

        env.owners_all.append({
            "docname": env.docname,
            "owners": owners,
        })

        # Store per-page metadata (recommended)
        env.metadata.setdefault(env.docname, {})
        env.metadata[env.docname]["owners"] = owners

        return []  # nothing rendered


def setup(app):
    app.add_directive("owners", OwnersDirective)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }