{
  config,
  lib,
  pkgs,
  ...
}:
with lib; let
  dooitWithPackages = pkgs.dooit.override {
    extraPackages = config.programs.dooit.extraPackages;
  };
in {
  options.programs.dooit = {
    enable = mkOption {
      type = types.bool;
      default = false;
      description = "Enable the Dooit TUI todo manager.";
    };
    extraPackages = mkOption {
      type = types.listOf types.package;
      default = [];
      description = "Extra packages to include with Dooit.";
    };
  };

  config = mkIf config.programs.dooit.enable {
    home.packages = [dooitWithPackages];
  };
}
