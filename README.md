# PyGVisuals
A collection of classes to create GUI's and more based purely on pygame (https://www.pygame.org/news).
Primarily supports python 3, but python 2 is also supposed to work with this.
(Works with both pygame 1.9.6 and pygame 2.)

_This is a byproduct of a larger, currently unactive and incomplete [project](https://github.com/AlinaGri/CoolesSpiel).
The classes now in PyGVisuals were developed by Impelon and kjkriegel._

___Note: Impelon currently maintains this project___

The project is (hopefully) well documented and includes most basic widgets.

## Helpful Links

- [Homepage](https://impelon.github.io/PyGVisuals/)
- [Documentation](https://impelon.github.io/PyGVisuals/api/)
- [GitHub](https://github.com/Impelon/PyGVisuals)
- Also check out [Pygame GUI](https://github.com/MyreMylar/pygame_gui) for a more modern and extensive GUI Library for pygame

## Help Wanted

Suggestions (& requests), bug-reports and contributions are welcome. If you have any ideas how to help me with this please comment on the respective issue.

I would be happy to see you use the contents of this repository. You are encouraged to open up a page on the Wiki showing how you use PyGVisuals in your projects.

## Screenshots/Examples

![bintree-gui](examples/bintree-gui/screenshot.png)
_A screenshot taken from the bintree-gui example_

## License

According to the [BSD-License](LICENSE.md) PyGVisuals is using, you can use the contents of this repository to your liking as long as you follow the license's terms and conditions.
If you want to include PyGVisuals or parts of it in your own project, include the files you need into your project's package (be sure to also include the [license](LICENSE.md)).
**Please note that not all parts of PyGVisuals are licensed under the [BSD-License](LICENSE.md).**
Content from third-parties which is embedded into PyGVisuals will be licensed under a separate license.
Here is a (potentially non-exhaustive) list of content which is not licensed with [PyGVisuals' license](LICENSE.md):
- The doc-inheritance mechanism is licensed under [Creative Commons Attribution-Share Alike](https://creativecommons.org/licenses/by-sa/4.0/). You can find a detailed disclaimer in the sourcecode.
- PyGVisuals' default font `Trueno` is licensed under [SIL Open Font License (OFL)](https://scripts.sil.org/cms/scripts/page.php?item_id=OFL_web). You can find a detailed copy of the license in the font's sourcefiles.

## Install

Currently to install this to your python-modules you need to download the project's sourcecode.
This can be done automatically via pip:

`pip install git+https://github.com/Impelon/PyGVisuals.git`

Or you can manually download it from GitHub or via git.

1. Download source and change directory into source: `git clone https://github.com/Impelon/PyGVisuals.git && cd PyGVisuals`
  - You can now test the library. Try out the examples via the start-script: `python start_example.py`
  - Additionally you can install your desired branch with this. List all available branches: `git branch`
  - Switch to desired branch: `git switch <branch>`
2. Install from current directory via pip: `python setup.py install`

## Epiloge

If you need help with using PyGVisuals, you can open an issue and I will try to help.
Also if you need any other features, you can also open an issue and add the label 'request'. I will work on new features that I think are worth adding.

Currently, because PyGVisuals is not actively used anywhere (I do not even use it myself), I do not have much motivation to add new features without any reasons.

__PyGVisuals requires [pygame](https://www.pygame.org/news) and obviously [python](https://www.python.org/) to work__
