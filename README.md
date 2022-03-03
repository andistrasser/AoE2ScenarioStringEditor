# AoE2ScenarioStringEditor

This tool gives you the possibility to edit the text content of an `aoe2scenario` file from **Age of Empires 2
Definitive Edition**
outside the in-game editor.

It can be used to translate scenarios in a quick and easy way or to make text changes after creating a scenario.

## Download

Windows:

[AoE2ScenarioStringEditor 1.0.6 (single-file application)](https://github.com/andistrasser/AoE2ScenarioStringEditor/raw/master/build/windows/AoE2ScenarioStringEditor_onefile.zip)

[AoE2ScenarioStringEditor 1.0.6](https://github.com/andistrasser/AoE2ScenarioStringEditor/raw/master/build/windows/AoE2ScenarioStringEditor_onedir.zip)

Linux:

[AoE2ScenarioStringEditor 1.0.6](https://github.com/andistrasser/AoE2ScenarioStringEditor/raw/master/build/linux/AoE2ScenarioStringEditor.zip)

## Documentation

[How to use AoE2ScenarioStringEditor](https://github.com/andistrasser/AoE2ScenarioStringEditor/blob/master/docs/DOC.md)

[How to translate a scenario](https://github.com/andistrasser/AoE2ScenarioStringEditor/blob/master/docs/TRANSLATE.md)

## Known Issues

- The single-file application may be detected as false positive by some antivirus software. This can't be avoided since
  I use PyInstaller for building the executable. You can either exclude AoE2ScenarioStringEditor.exe in your antivirus
  software or you can download the non-single-file application which should make no problems.
- Opening scenarios of different versions in the same instance doesn't work at the moment. This issue is caused by the
  AoE2ScenarioParser library and will be fixed in the future. (Workaround: Close AoE2ScenarioStringEditor, reopen it and
  it will work again)

## Changelog

Detailed info about bug fixes and progress can be found in
the [CHANGELOG](https://github.com/andistrasser/AoE2ScenarioStringEditor/blob/master/CHANGELOG.md) file.

## Author

- Andreas Strasser

## Credits

Special thanks to [Kerwin Sneijders](https://github.com/KSneijders) for providing
the [AoE2ScenarioParser](https://github.com/KSneijders/AoE2ScenarioParser) library.

## License

GNU General Public License v3.0: Please see
the [LICENSE](https://github.com/andistrasser/AoE2ScenarioStringEditor/blob/master/LICENSE) file.