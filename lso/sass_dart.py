import os, subprocess

from webassets.filter import ExternalTool
from webassets.cache import FilesystemCache


__all__ = ("Sass", "SCSS")


class SassDart(ExternalTool):  # pragma: no cover
    """Modified version of webassets' default :class:`Sass` filter,
    to support the new Dart version.
    """

    name = "sass-dart"
    options = {
        "binary": "SASS_BIN",
        "debug_info": "SASS_DEBUG_INFO",
        "as_output": "SASS_AS_OUTPUT",
        "load_paths": "SASS_LOAD_PATHS",
        "libs": "SASS_LIBS",
        "style": "SASS_STYLE",
    }
    max_debug_level = None

    def resolve_path(self, path):
        return self.ctx.resolver.resolve_source(self.ctx, path)

    def _apply_sass(self, _in, out, cd=None):
        # Switch to source file directory if asked, so that this directory
        # is by default on the load path. We could pass it via -I, but then
        # files in the (undefined) wd could shadow the correct files.
        orig_cwd = os.getcwd()
        child_cwd = orig_cwd
        if cd:
            child_cwd = cd

        args = [self.binary or "sass", "--stdin", "--style", self.style or "expanded"]
        if self.ctx.environment.debug if self.debug_info is None else self.debug_info:
            args.append("--debug-info")
        for path in self.load_paths or []:
            if os.path.isabs(path):
                abs_path = path
            else:
                abs_path = self.resolve_path(path)
            args.extend(["-I", abs_path])
        for lib in self.libs or []:
            if os.path.isabs(lib):
                abs_path = lib
            else:
                abs_path = self.resolve_path(lib)
            args.extend(["-r", abs_path])

        return self.subprocess(args, out, _in, cwd=child_cwd)

    def input(self, _in, out, source_path, output_path, **kw):
        if self.as_output:
            out.write(_in.read())
        else:
            self._apply_sass(_in, out, os.path.dirname(source_path))

    def output(self, _in, out, **kwargs):
        if not self.as_output:
            out.write(_in.read())
        else:
            self._apply_sass(_in, out)
