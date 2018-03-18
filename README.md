This is my RPM package for [mu](http://www.djcbsoftware.nl/code/mu/) and
[mu4e](http://www.djcbsoftware.nl/code/mu/mu4e.html). This is a little different
from the one in the mu `contrib` directory of mu, I'm trying to modernize it.
You can find the packages I've built in my [Fedora
Copr](https://copr.fedorainfracloud.org/coprs/eklitzke/mu/).

The spec file (or SPRM) will build three packages: `mu`, `mu-guile`, and
`emacs-mu4e`.

The `mu` package installs the command of the same time (a tool for indexing mail
directories).

The `emacs-mu4e` package installs the Emacs mu4e package, which is a mail reader
for Emacs.

The `mu-guile` package installs Scheme language bindings for Guile. These
provide additional `mu script` commands, and I recommend you install this
package if you are using mu.
