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
            this.Monitor.Log("开始更新和部署翻译文件...", LogLevel.Info);
            
            string modsDir = Path.GetDirectoryName(Helper.DirectoryPath);
            int collectedCount = 0;
            int deployedCount = 0;
            int scannedCount = 0;
            
            if (!Directory.Exists(modsDir))
            {
                this.Monitor.Log("找不到Mods文件夹", LogLevel.Error);
                return;
            }
            
            // 第一步：递归收集所有模组的 default.json 文件
            this.Monitor.Log("正在收集模组的默认翻译文件...", LogLevel.Info);
            ScanModsRecursively(modsDir, ref collectedCount, ref scannedCount, true);
            
            this.Monitor.Log($"收集完成！从 {collectedCount} 个模组收集了默认翻译文件", LogLevel.Info);
            
            // 第二步：递归部署翻译文件
            this.Monitor.Log("正在部署中文翻译文件...", LogLevel.Info);
            deployedCount = 0; // 重置计数器
            ScanModsRecursively(modsDir, ref deployedCount, ref scannedCount, false);
            
            this.Monitor.Log($"部署完成！扫描了 {scannedCount} 个模组，收集了 {collectedCount} 个默认文件，部署了 {deployedCount} 个翻译文件", LogLevel.Info);
        }

        private void ScanModsRecursively(string directory, ref int actionCount, ref int scannedCount, bool isCollecting)
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
                            bool success = false;
                            if (isCollecting)
                            {
                                success = CollectDefaultTranslation(modId, subDir);
                            }
                            else
                            {
                                success = DeployTranslationToMod(modId, subDir);
                            }
                            
                            if (success)
                            {
                                actionCount++;
                            }
                        }
                    }
                    
                    // 递归搜索子文件夹
                    ScanModsRecursively(subDir, ref actionCount, ref scannedCount, isCollecting);
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

        private bool CollectDefaultTranslation(string modId, string modPath)
        {
            try
            {
                string modI18nPath = Path.Combine(modPath, "i18n");
                
                if (!Directory.Exists(modI18nPath))
                {
                    this.Monitor.Log($"模组 {modId} 没有i18n文件夹", LogLevel.Debug);
                    return false;
                }
                
                string defaultFile = Path.Combine(modI18nPath, "default.json");
                if (!File.Exists(defaultFile))
                {
                    this.Monitor.Log($"模组 {modId} 没有default.json文件", LogLevel.Debug);
                    return false;
                }
                
                // 确保我们的translations文件夹存在
                string myTranslationsPath = Path.Combine(Helper.DirectoryPath, "translations", modId);
                if (!Directory.Exists(myTranslationsPath))
                {
                    Directory.CreateDirectory(myTranslationsPath);
                    this.Monitor.Log($"为模组 {modId} 创建翻译文件夹", LogLevel.Debug);
                }
                
                // 复制 default.json
                string targetDefault = Path.Combine(myTranslationsPath, "default.json");
                File.Copy(defaultFile, targetDefault, true);
                
                this.Monitor.Log($"更新模组 {modId} 的default.json", LogLevel.Debug);
                return true;
            }
            catch (System.Exception ex)
            {
                this.Monitor.Log($"收集模组 {modId} 默认翻译失败: {ex.Message}", LogLevel.Error);
                return false;
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