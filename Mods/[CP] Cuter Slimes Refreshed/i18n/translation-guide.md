# Translation Guide for "Cuter Slimes Refreshed"

Thank you for helping translate this mod! This guide will help you understand the translation structure and any special considerations.

## File Structure

Place your translation file in the `i18n` folder with the appropriate language code:
```
i18n/
├── default.json    (English - required)
├── de.json        (German)
├── es.json        (Spanish)
├── fr.json        (French)
├── etc...
```

## Translation Keys

### Config Section Headers
```json
"config.section.General.name": "General Settings",
"config.section.Appearance.name": "Appearance Settings"
```
These are section headers in the mod's configuration menu.

### Config Options

1. Enable/Disable Feature:
```json
"config.Enabled.name": "Enable Cute Slimes",
"config.Enabled.description": "Turn this on to make all your slimes look cuter than ever.",
"config.Enabled.values.true": "Yes",
"config.Enabled.values.false": "No"
```

2. Slime Style Selection:
```json
"config.Mode.name": "Slime Style",
"config.Mode.description": "Choose how you want your slimes to look. Jelly makes them look more squishy and translucent, while Glossy gives them a shiny, reflective appearance.",
"config.Mode.values.jelly": "Jelly",
"config.Mode.values.glossy": "Glossy"
```

### Special Considerations

1. **Game Terms**: 
   - Don't translate "Slime" unless it has an official translation in your language's version of Stardew Valley
   - Keep style names "Jelly" and "Glossy" consistent with any existing translations in your language

2. **Descriptions**:
   - Maintain the friendly, descriptive tone
   - Keep visual descriptions accurate (e.g., "squishy", "translucent", "shiny", "reflective")
   - Ensure the difference between styles is clear in your translation

3. **Formatting**: 
   - Keep the `.name`, `.description`, and `.values` suffixes unchanged
   - Maintain any special characters or formatting
   - Preserve capitalization where appropriate

4. **Style Names**:
   - If your language has established translations for "Jelly" and "Glossy" in other mods or games, consider using those
   - If not, choose terms that best convey the visual appearance in your language

### Testing Your Translation

1. Place your translation file in the i18n folder
2. Launch the game and set it to your language
3. Check:
   - Mod configuration menu
   - All option descriptions
   - Style names in the dropdown menu
4. Verify all text displays correctly and makes sense in context

### Need Help?

If you need clarification or help with your translation:
1. Check the default.json file for reference
2. Create an issue on the mod's Nexus page
3. Contact the active mod author (JennaJuffuffles)

## Translation Status

Current translations:
- English (default.json)
- German (de.json)
- Spanish (es.json)
- French (fr.json)
- Hungarian (hu.json)
- Italian (it.json)
- Japanese (ja.json)
- Korean (ko.json)
- Polish (pl.json) by Naciux1088
- Portuguese (pt.json)
- Russian (ru.json)
- Turkish (tr.json)
- Chinese (zh.json)
- [Add other completed translations here]

## Version History

Keep track of which version of the mod your translation is for:
- v1.0.3: Current release
- [Add future versions here] 