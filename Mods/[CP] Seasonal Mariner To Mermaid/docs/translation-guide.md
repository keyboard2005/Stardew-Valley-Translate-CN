# Translation Guide for "Seasonal Mariner to Mermaid"

Thank you for helping translate this mod! This guide will help you understand the translation structure and any special considerations.

## Current Translations & Translators

- English (default.json)
- Chinese (zh.json) by vocal688
- German (de.json) by Blackwood10
- French (fr.json) by Fsecho7
- Japanese (ja.json) by mitekano23
- Korean (ko.json) by cab0105
- Portuguese (pt.json) by Maatsuki
- Russian (ru.json) by nightowl2012
- Spanish (es.json) by ArazRed
- Thai (th.json) by valkyire11ll

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

## JSON Formatting

1. **File Header**:
   - Do not include comments in the JSON file as they are not valid JSON syntax
   - Instead, document your translation credits in the README or a separate credits file
   - Example:
   ```json
   {
     "config.enabled.name": "Enable Mod",
     ...
   }
   ```

2. **Basic JSON Rules**:
   - Use double quotes `"` for all strings
   - No trailing commas after the last item
   - Keep the same key structure as default.json
   - Maintain proper indentation (2 spaces)
   - Keep the file as valid JSON (no comments allowed)

3. **Line Breaks**:
   - Use `\n` for line breaks in text
   - Example: `"MarriageSecretBook": "Line 1\nLine 2\nLine 3"`

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
"config.Enabled.name": "Enable Mod",
"config.Enabled.description": "Replace the Old Mariner with a seasonal mermaid visitor.",
"config.Enabled.value.true": "Yes",
"config.Enabled.value.false": "No"
```

2. Custom Names:
```json
"config.UseCustomNames.name": "Use Custom Names",
"config.UseCustomNames.description": "Use custom names for each seasonal mermaid.",
"config.UseCustomNames.value.true": "Yes",
"config.UseCustomNames.value.false": "No"
```

3. Seasonal Mermaid Names:
```json
"config.CustomSpringName.name": "Spring Mermaid Name",
"config.CustomSpringName.description": "Custom name for the Spring mermaid.",
"config.CustomSummerName.name": "Summer Mermaid Name",
"config.CustomSummerName.description": "Custom name for the Summer mermaid.",
"config.CustomFallName.name": "Fall Mermaid Name",
"config.CustomFallName.description": "Custom name for the Fall mermaid.",
"config.CustomWinterName.name": "Winter Mermaid Name",
"config.CustomWinterName.description": "Custom name for the Winter mermaid."
```

### Dialogue and Text

1. Basic Interactions:
```json
"MermaidBuyNo": "Not now...",
"MermaidBuyPrompt": "Buy Mermaid's Pendant?",
"MermaidBuyYes": "Buy (5000g)",
"MermaidLine": "Do you seek my pendant?"
```

2. Seasonal Dialogue:
Each season has its own set of dialogue for different weather conditions and situations. The structure follows:
```json
"[season].[weather].[action]": "Dialogue text"
```
For example:
```json
"spring.Rain.MermaidBuyNoAnswer": "No rush. Love takes time.",
"spring.Rain.MermaidBuyYesAnswer": "Take it, and let your love bloom.",
"spring.Rain.buyItemQuestion": "Sprynglynn: Do you seek my pendant?"
```

3. Marriage Guide Book:
```json
"MarriageSecretBook": "Marriage Guide For Farmers\nBefore you ask someone to marry you..."
```

### Special Considerations

1. **Character Names**:
   - Keep the default mermaid names (Sprynglynn, Sunneigh, Pumpkyn, Glaciaire) consistent with the English version
   - If translating custom names, maintain the playful nature of the original names
   - Consider cultural appropriateness when translating names

2. **Weather-Specific Content**:
   - Maintain the connection between weather and dialogue
   - Keep the emotional tone appropriate for each weather condition
   - Ensure weather descriptions match the game's terminology in your language

3. **Marriage Guide**:
   - Keep the format of the marriage guide consistent
   - Maintain the line breaks (\n) as they appear in the original
   - Keep game-specific terms consistent with your language's version of Stardew Valley

4. **Formatting**:
   - Keep the `.name`, `.description`, and `.value` suffixes unchanged
   - Maintain any special characters or formatting
   - Preserve line breaks in the marriage guide
   - Keep the seasonal and weather structure intact

### Testing Your Translation

1. Place your translation file in the i18n folder
2. Launch the game and set it to your language
3. Check:
   - Mod configuration menu
   - All option descriptions
   - Seasonal mermaid dialogue
   - Marriage guide text
   - Weather-specific interactions
4. Verify all text displays correctly and makes sense in context

### Need Help?

If you need clarification or help:
1. Check the default.json file for reference
2. Contact the active mod author (JennaJuffuffles) via Nexus DM

[list]
[*]🇨🇳 zh/简体中文翻译由[url=https://next.nexusmods.com/profile/vocal688/about-me]vocal688[/url]提供！
[*]🇧🇷 pt/Tradução pt fornecida por [url=https://next.nexusmods.com/profile/Maatsuki/about-me]Maatsuki[/url]!
[*]🇷🇺 ru/Русский перевод предоставлен [url=https://next.nexusmods.com/profile/nightowl2012/about-me]nightowl2012[/url]!
[*]🇪🇸 es/traducción al español proporcionada por [url=https://next.nexusmods.com/profile/ArazRed/about-me]ArazRed[/url]!
[*]🇯🇵 ja/日本語翻訳提供：[url=https://next.nexusmods.com/profile/mitekano23/about-me]mitekano23[/url]!
[*]🇹🇭 th/แปลไทยโดย [url=https://www.nexusmods.com/users/43454257]valkyire11ll[/url]! ([url=https://www.nexusmods.com/stardewvalley/mods/7052]คลิกที่นี่เพื่อดูความต้องการ[/url])
[*]🇫🇷 fr/Traduction française fournie par [url=https://next.nexusmods.com/profile/Fsecho7/about-me]Fsecho7[/url]!
[*]🇰🇷 kr/[url=https://next.nexusmods.com/profile/cab0105/about-me]cab0105[/url]﻿의 번역!
[*]🇩🇪 de/Deutsche Übersetzung von [url=https://next.nexusmods.com/profile/Blackwood10/about-me]Blackwood10[/url]!
[/list]
