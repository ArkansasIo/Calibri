using UnrealBuildTool;

public class CalibriAI : ModuleRules
{
    public CalibriAI(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] { "Core" });
        PrivateDependencyModuleNames.AddRange(new[] { "CoreUObject", "Engine" });
    }
}
