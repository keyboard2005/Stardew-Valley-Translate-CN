# Translation Guide for "Tiny Totem Statue Obelisks"

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
"config.section.Appearance.name": "Appearance Settings",
"config.section.MiniObelisks.name": "Mini-Obelisk Settings",
"config.section.Remote.name": "Remote Obelisk Settings",
"config.section.Compatibility.name": "Mod Compatibility"
```
These are section headers in the mod's configuration menu.

### Config Options

1. Obelisk Toggles:
```json
"config.EarthObeliskEnabled.name": "Enable Earth Obelisk",
"config.EarthObeliskEnabled.description": "Toggle to enable or disable retexturing of Earth Obelisk on the farm.",
"config.EarthObeliskEnabled.values.true": "Yes",
"config.EarthObeliskEnabled.values.false": "No",

"config.DesertObeliskEnabled.name": "Enable Desert Obelisk",
"config.DesertObeliskEnabled.description": "Toggle to enable or disable retexturing of Desert Obelisk on the farm.",
"config.DesertObeliskEnabled.values.true": "Yes",
"config.DesertObeliskEnabled.values.false": "No"
```
Similar patterns exist for Water, Island, and Farm Obelisks.

2. Decoration Options:
```json
"config.FlowersEnabled.name": "Enable Flowers",
"config.FlowersEnabled.description": "Toggle to enable or disable flowers decoration.",
"config.FlowersEnabled.values.true": "Yes",
"config.FlowersEnabled.values.false": "No",

"config.MossEnabled.name": "Enable Moss",
"config.MossEnabled.description": "Toggle to enable or disable moss decoration.",
"config.MossEnabled.values.true": "Yes",
"config.MossEnabled.values.false": "No"
```

3. Mini-Obelisk Settings:
```json
"config.MiniObeliskEnabled.name": "Enable Mini-Obelisk",
"config.MiniObeliskEnabled.description": "Toggle to enable or disable retexturing of Mini-Obelisk.",
"config.MiniObeliskEnabled.values.true": "Yes",
"config.MiniObeliskEnabled.values.false": "No",

"config.MiniObeliskStyle.name": "Mini-Obelisk Style",
"config.MiniObeliskStyle.description": "Choose the style for all Mini-Obelisks.",
"config.MiniObeliskStyle.values.signpost": "Signpost"
```

### Special Considerations

1. **Game Terms**: 
   - Obelisk names ("Earth Obelisk", "Desert Obelisk", etc.) should match the terms used in your language's version of Stardew Valley
   - Keep obelisk type names consistent with the game's official translation
   - "Mini-Obelisk" should be translated consistently throughout

2. **Style Names**:
   - Style names like "Signpost" should be translated to maintain their descriptive meaning
   - Keep translations consistent with the visual appearance of the style

3. **Formatting**: 
   - Keep the `.name`, `.description`, and `.values` suffixes unchanged
   - Maintain any special characters or formatting
   - Keep capitalization appropriate for your language
   - Preserve spaces in key names (e.g., "Earth Obelisk" must keep the space)

4. **Descriptions**:
   - Keep descriptions clear and concise
   - Maintain the relationship between toggles and their effects
   - Be consistent in describing "retexturing" functionality

### Testing Your Translation

1. Place your translation file in the i18n folder
2. Launch the game and set it to your language
3. Check:
   - Mod configuration menu
   - All obelisk type names
   - Toggle descriptions
   - Style options
   - Decoration settings
4. Verify all text displays correctly and makes sense in context

### Need Help?

If you need clarification or help with your translation:
1. Check the default.json file for reference
2. Create an issue on the mod's Nexus page
3. Contact the mod author (JennaJuffuffles)

## Translation Status

Current translations:
- English (default.json)
- [Add other completed translations here]

## Version History

Keep track of which version of the mod your translation is for:
- v1.2.0: Current release
- [Add future versions here] 