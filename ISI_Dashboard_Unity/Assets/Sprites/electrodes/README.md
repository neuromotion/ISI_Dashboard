## Batch convert svg|pdf|eps|emf|wmf|ai|ps to eps|pdf|png|svg|ps|emf|wmf
![Screenshot](https://i.imgur.com/tmN6zXe.png)
*Batch converter for Windows using Inkscape with the command line*  
InkscapeBatchConvert is an easy to use solution to quickly convert all files of a folder to another type without the need to open Inkscape. The program uses Windows Batch scripting and will only work on Windows.  
Tested with Inkscape 0.9.x - 1.3.x ✅

## Usage
1. Download `_InkscapeBatchConvert.bat`
2. Put it in the folder where you have files you wish to convert.
3. Then double click the file to start it.

## Troubleshooting

| Problem                                                      | Solution                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Windows blocks the program                                   | `Right click the file → Properties → Unblock`                |
| ![Windows protected your PC](https://i.imgur.com/fSAJXh0.png) | ![Disable blocking](https://i.imgur.com/2SBAyuv.png)         |
| I can't convert EPS / PDF files. The program says it runs the conversion, but there are no files in the out folder. | Make sure you have ghost script installed and added to your environment path. For more information read the [Inkscape FAQ](https://inkscape.org/learn/faq/#how-open-eps-files-windows) |
|                                                              | ![Add ghostscript to path](https://i.imgur.com/aw59Zis.png)  |
| Can't find Inkscape installation                             | All common file paths are checked for the installation. If you haven't installed Inkscape download it [here](https://inkscape.org/download), otherwise you can also define your own path in the script by adding the next array element of `inkscapePaths` to the script |
| ![Can't find inkscape installation](https://i.imgur.com/thIao2h.png) | ![custom inkscape path](https://i.imgur.com/ALZUBsl.png)     |
| I'm missing a setting in the script, e.g. defined output width | Have a look at the [Commandline Documentation](https://wiki.inkscape.org/wiki/index.php/Using_the_Command_Line) or read the inkscape help file `inkscape --help` and add the needed properties to the script |
| ![Inkscape help output](https://i.imgur.com/PHublJx.png)     | ![Script change position](https://i.imgur.com/fNeaz8j.png)   |
| I'm missing a specific input or output type                  | If inkscape supports those types, you can easily add them to the list in the script (search for `validInput` and `validOutput`) |
|                                                              | ![Add input / output type](https://i.imgur.com/yE0kIaH.png)  |

## Todo

Use shell or pipe to avoid starting inkscape for every file as pointed out by @vaifrax [here](https://gist.github.com/JohannesDeml/779b29128cdd7f216ab5000466404f11#gistcomment-2697671). I would be very happy to get help for that 🙂

## Credits

* [JohannesDeml](https://github.com/JohannesDeml)
* [Elrinth](https://github.com/Elrinth)
* [leifcr](https://github.com/leifcr)