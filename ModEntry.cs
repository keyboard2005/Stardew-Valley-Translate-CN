using StardewModdingAPI;
using StardewModdingAPI.Events;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

namespace TranslateAll
{
    public class ModEntry : Mod
    {
        public override void Entry(IModHelper helper)
        {
            this.Monitor.Log("TranslateAll 启动 - i18n翻译文件部署模式", LogLevel.Info);
            
            helper.Events.GameLoop.GameLaunched += OnGameLaunched;
        }

        private void OnGameLaunched(object sender, GameLaunchedEventArgs e)
        {
            this.Monitor.Log("开始部署中文翻译文件...", LogLevel.Info);
            
            string modsDir = Path.GetDirectoryName(Helper.DirectoryPath);
            int deployedCount = 0;
            int scannedCount = 0;
            
            if (!Directory.Exists(modsDir))
            {
                this.Monitor.Log("找不到Mods文件夹", LogLevel.Error);
                return;
            }
            
            // 递归部署翻译文件
            ScanModsRecursively(modsDir, ref deployedCount, ref scannedCount);
            
            this.Monitor.Log($"部署完成！扫描了 {scannedCount} 个模组，成功部署了 {deployedCount} 个中文翻译文件", LogLevel.Info);
        }

        private void ScanModsRecursively(string directory, ref int deployedCount, ref int scannedCount)
        {
            try
            {
                foreach (string subDir in Directory.GetDirectories(directory))
                {
                    string dirName = Path.GetFileName(subDir);
                    
                    // 跳过自己的模组文件夹
                    if (dirName == Path.GetFileName(Helper.DirectoryPath))
                        continue;
                    
                    // 检查当前文件夹是否是模组（有manifest.json）
                    string manifestPath = Path.Combine(subDir, "manifest.json");
                    if (File.Exists(manifestPath))
                    {
                        scannedCount++;
                        string modId = GetModIdFromFolder(subDir);
                        
                        if (!string.IsNullOrEmpty(modId))
                        {
                            if (DeployTranslationToMod(modId, subDir))
                            {
                                deployedCount++;
                            }
                        }
                    }
                    
                    // 递归搜索子文件夹
                    ScanModsRecursively(subDir, ref deployedCount, ref scannedCount);
                }
            }
            catch (System.Exception ex)
            {
                this.Monitor.Log($"扫描文件夹 {directory} 时出错: {ex.Message}", LogLevel.Error);
            }
        }

        private string GetModIdFromFolder(string modFolderPath)
        {
            try
            {
                string manifestPath = Path.Combine(modFolderPath, "manifest.json");
                
                if (!File.Exists(manifestPath))
                {
                    this.Monitor.Log($"模组文件夹 {Path.GetFileName(modFolderPath)} 没有manifest.json文件", LogLevel.Debug);
                    return null;
                }
                
                string manifestJson = File.ReadAllText(manifestPath);
                dynamic manifest = JsonConvert.DeserializeObject(manifestJson);
                
                if (manifest?.UniqueID != null)
                {
                    return manifest.UniqueID.ToString();
                }
                
                this.Monitor.Log($"模组文件夹 {Path.GetFileName(modFolderPath)} 的manifest.json中没有UniqueID", LogLevel.Debug);
                return null;
            }
            catch (System.Exception ex)
            {
                this.Monitor.Log($"读取模组 {Path.GetFileName(modFolderPath)} 的manifest.json失败: {ex.Message}", LogLevel.Debug);
                return null;
            }
        }

        private bool DeployTranslationToMod(string modId, string modPath)
        {
            string myTranslationFile = Path.Combine(Helper.DirectoryPath, "translations", modId, "zh.json");
            
            if (!File.Exists(myTranslationFile))
            {
                this.Monitor.Log($"没有找到模组 {modId} 的翻译文件", LogLevel.Debug);
                return false;
            }

            try
            {
                // 直接读取本地翻译文件
                string translationJson = File.ReadAllText(myTranslationFile);
                var translations = JsonConvert.DeserializeObject<Dictionary<string, string>>(translationJson);
                
                if (translations == null || translations.Count == 0)
                {
                    this.Monitor.Log($"模组 {modId} 的翻译文件为空", LogLevel.Debug);
                    return false;
                }

                string modI18nPath = Path.Combine(modPath, "i18n");
                if (!Directory.Exists(modI18nPath))
                {
                    Directory.CreateDirectory(modI18nPath);
                    this.Monitor.Log($"为模组 {modId} 创建了 i18n 文件夹", LogLevel.Debug);
                }

                string targetFile = Path.Combine(modI18nPath, "zh.json");
                
                // 直接覆盖写入翻译文件
                File.WriteAllText(targetFile, translationJson);
                
                this.Monitor.Log($"成功为模组 {modId} ({Path.GetFileName(modPath)}) 部署中文翻译 ({translations.Count} 条)", LogLevel.Info);
                return true;
            }
            catch (System.Exception ex)
            {
                this.Monitor.Log($"为模组 {modId} 部署翻译文件失败: {ex.Message}", LogLevel.Error);
                return false;
            }
        }
    }
}