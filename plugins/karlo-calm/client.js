window.__ModuleLoader__.load({
  id: "@local/karlo-calm",
  factory(require) {
    var TOKENS = {
  "--dsw-alias-bg-base": {
    "light": "#F6F4ED",
    "dark": "#293D32"
  },
  "--dsw-alias-bg-layer-1": {
    "light": "#FFFEFA",
    "dark": "#31453A"
  },
  "--dsw-alias-bg-layer-2": {
    "light": "#FBF9F1",
    "dark": "#364B3F"
  },
  "--dsw-alias-bg-layer-3": {
    "light": "#F3F0E5",
    "dark": "#3C5245"
  },
  "--dsw-alias-bg-overlay": {
    "light": "#FFFEFA",
    "dark": "#31453A"
  },
  "--dsw-alias-bg-module-platform": {
    "light": "#F1EEE3",
    "dark": "#3A4E42"
  },
  "--dsw-alias-bg-multi-select": {
    "light": "#F1EEE3",
    "dark": "#3A4E42"
  },
  "--dsw-alias-bg-skeleton": {
    "light": "#252A260D",
    "dark": "#F6F4ED1A"
  },
  "--dsw-alias-bg-document-preview": {
    "light": "#EFECE1",
    "dark": "#223129"
  },
  "--dsw-alias-label-document-preview": {
    "light": "#63685C",
    "dark": "#C4CCBC"
  },
  "--dsw-alias-bg-document-selection": {
    "light": "#B8614640",
    "dark": "#C9805F52"
  },
  "--dsw-alias-bg-mask-1": {
    "light": "#1C17103D",
    "dark": "#0C141080"
  },
  "--dsw-alias-bg-mask-2": {
    "light": "#1C17101F",
    "dark": "#0C141033"
  },
  "--dsw-alias-bg-mask-3": {
    "light": "#1C17107A",
    "dark": "#0C14107A"
  },
  "--dsw-alias-bg-mask-photo": {
    "light": "#14110CE0",
    "dark": "#080D0AE0"
  },
  "--dsw-alias-bg-mask-drop": {
    "light": "#F6F4EDB3",
    "dark": "#223129B3"
  },
  "--dsw-alias-border-l1": {
    "light": "#E5E4DD",
    "dark": "#35483D"
  },
  "--dsw-alias-border-l2": {
    "light": "#DDDCD5",
    "dark": "#425348"
  },
  "--dsw-alias-border-l2-darkmode-thin": {
    "light": "#DDDCD5",
    "dark": "#35483D"
  },
  "--dsw-alias-border-l3": {
    "light": "#D5D4CD",
    "dark": "#4A5A50"
  },
  "--dsw-alias-border-l4": {
    "light": "#C8C8C1",
    "dark": "#5A695F"
  },
  "--dsw-alias-border-inverted": {
    "light": "#00000000",
    "dark": "#F6F4ED14"
  },
  "--dsw-alias-border-inverted2": {
    "light": "#00000000",
    "dark": "#F6F4ED1F"
  },
  "--dsw-alias-brand-primary": {
    "light": "#252A26",
    "dark": "#F6F4ED"
  },
  "--dsw-alias-brand-primary-invert": {
    "light": "#252A26",
    "dark": "#F6F4ED"
  },
  "--dsw-alias-brand-text": {
    "light": "#252A26",
    "dark": "#F6F4ED"
  },
  "--dsw-alias-brand-primary-new-colorprimary-new-color": {
    "light": "#B86146",
    "dark": "#C9805F"
  },
  "--dsw-alias-button-primary-fill": {
    "light": "#252A26",
    "dark": "#F6F4ED"
  },
  "--dsw-alias-button-primary-hover": {
    "light": "#3C423B",
    "dark": "#FFFFFF"
  },
  "--dsw-alias-button-primary-dimmed": {
    "light": "#E9E4D6",
    "dark": "#3A4E42"
  },
  "--dsw-alias-button-contrast-fill": {
    "light": "#565B52",
    "dark": "#DCE1D4"
  },
  "--dsw-alias-button-elevated-fill": {
    "light": "#FFFEFA",
    "dark": "#31453A"
  },
  "--dsw-alias-button-floating-fill": {
    "light": "#FFFEFA",
    "dark": "#2A3C31"
  },
  "--dsw-alias-button-floating-hover": {
    "light": "#F1EEE3",
    "dark": "#31453A"
  },
  "--dsw-alias-button-ghost-active-border": {
    "light": "#8B9082",
    "dark": "#5E7163"
  },
  "--dsw-alias-button-ghost-active-fill": {
    "light": "#EDEAE0",
    "dark": "#31453A"
  },
  "--dsw-alias-button-ghost-active-hover": {
    "light": "#E5E1D3",
    "dark": "#3A4E42"
  },
  "--dsw-alias-button-info-fill": {
    "light": "#A5553B",
    "dark": "#D08A6C"
  },
  "--dsw-alias-button-info-hover": {
    "light": "#94492F",
    "dark": "#D89A7E"
  },
  "--dsw-alias-button-tool-bar-fill": {
    "light": "#565B5280",
    "dark": "#3A4E4280"
  },
  "--dsw-alias-button-tool-bar-hover": {
    "light": "#565B5299",
    "dark": "#3A4E4299"
  },
  "--dsw-alias-button-tool-bar-fill-invisible": {
    "light": "#252A261A",
    "dark": "#1F2A225C"
  },
  "--dsw-alias-interactive-bg-hover": {
    "light": "#252A260F",
    "dark": "#F6F4ED14"
  },
  "--dsw-alias-interactive-bg-active": {
    "light": "#252A261A",
    "dark": "#F6F4ED24"
  },
  "--dsw-alias-interactive-bg-hover-accent": {
    "light": "#B8614624",
    "dark": "#C9805F3D"
  },
  "--dsw-alias-interactive-bg-hover-danger": {
    "light": "#B0392C0D",
    "dark": "#E0826D26"
  },
  "--dsw-alias-interactive-bg-hover-solid": {
    "light": "#ECE9DD",
    "dark": "#3A4E42"
  },
  "--dsw-alias-label-primary": {
    "light": "#252A26",
    "dark": "#F6F4ED"
  },
  "--dsw-alias-label-secondary": {
    "light": "#666A62",
    "dark": "#C4CCBC"
  },
  "--dsw-alias-label-tertiary": {
    "light": "#5E635A",
    "dark": "#AEB8A8"
  },
  "--dsw-alias-label-caption": {
    "light": "#5E635A",
    "dark": "#9CA696"
  },
  "--dsw-alias-label-dimmed": {
    "light": "#9C9F91",
    "dark": "#71806F"
  },
  "--dsw-alias-label-primary-dimmed": {
    "light": "#2E332E",
    "dark": "#DCE1D4"
  },
  "--dsw-alias-label-primary-bluish": {
    "light": "#293D32",
    "dark": "#F6F4ED"
  },
  "--dsw-alias-label-primary-foreground": {
    "light": "#F6F4ED",
    "dark": "#1F2A22"
  },
  "--dsw-alias-label-primary-inverted": {
    "light": "#F6F4ED",
    "dark": "#26332A"
  },
  "--dsw-alias-label-shimmer": {
    "light": "#0000004D",
    "dark": "#FFFFFF73"
  },
  "--dsw-alias-label-deep-diving": {
    "light": "color-mix(in srgb, #B86146 70%, #3A241C)",
    "dark": "color-mix(in srgb, #C9805F 70%, #F6F4ED)"
  },
  "--dsw-alias-label-deep-diving-shimmer": {
    "light": "color-mix(in srgb, #B86146 30%, #3A241C)",
    "dark": "color-mix(in srgb, #E0A284 75%, #F6F4ED)"
  },
  "--dsw-alias-menu-icon": {
    "light": "#3C423B",
    "dark": "#DCE1D4"
  },
  "--dsw-alias-link": {
    "light": "#9E4E33",
    "dark": "#DEA488"
  },
  "--dsw-alias-markdown-citation": {
    "light": "#EAE6D8",
    "dark": "#31453A"
  },
  "--dsw-alias-markdown-code-block": {
    "light": "#F0EDE2",
    "dark": "#1F2A22"
  },
  "--dsw-alias-markdown-code-block-banner": {
    "light": "#F0EDE2",
    "dark": "#26332A"
  },
  "--dsw-alias-markdown-code-segment-selected": {
    "light": "#FFFEFA",
    "dark": "#31453A"
  },
  "--dsw-alias-markdown-code-segment-unselected": {
    "light": "#E9E5D8",
    "dark": "#243529"
  },
  "--dsw-alias-markdown-inline-code": {
    "light": "#EFECE1",
    "dark": "#2A3C31"
  },
  "--dsw-alias-markdown-placeholder": {
    "light": "#EFECE1",
    "dark": "#2E4136"
  },
  "--dsw-alias-markdown-tag": {
    "light": "#E9E5D8",
    "dark": "#26332A"
  },
  "--dsw-alias-scrollbar-bg-l1": {
    "light": "#D9D4C5",
    "dark": "#4E5D50"
  },
  "--dsw-alias-scrollbar-bg-l2": {
    "light": "#D9D4C5",
    "dark": "#465548"
  },
  "--dsw-alias-scrollbar-hover-l1": {
    "light": "#C9C3B2",
    "dark": "#5E6D5F"
  },
  "--dsw-alias-scrollbar-hover-l2": {
    "light": "#C9C3B2",
    "dark": "#566550"
  },
  "--dsw-alias-state-business-primary": {
    "light": "#B86146",
    "dark": "#C9805F"
  },
  "--dsw-alias-state-business-tertiary": {
    "light": "#F0DCCE",
    "dark": "#3A2C24"
  },
  "--dsw-alias-state-error-primary": {
    "light": "#B0392C",
    "dark": "#E68F7B"
  },
  "--dsw-alias-state-error-secondary": {
    "light": "#C9503F",
    "dark": "#E68F7B"
  },
  "--dsw-alias-state-idle-primary": {
    "light": "#D8D3C4",
    "dark": "#55645A"
  },
  "--dsw-alias-state-success-primary": {
    "light": "#33684A",
    "dark": "#83BB97"
  },
  "--dsw-alias-state-success-secondary": {
    "light": "#4E8A66",
    "dark": "#6FA983"
  },
  "--dsw-alias-state-success-tertiary": {
    "light": "#DFEAE0",
    "dark": "#1F3529"
  },
  "--dsw-alias-state-warn-primary": {
    "light": "#B27C1F",
    "dark": "#D9A94F"
  },
  "--dsw-alias-state-warn-secondary": {
    "light": "#C99B3F",
    "dark": "#C19340"
  },
  "--dsw-alias-state-warn-tertiary": {
    "light": "#F6EBD2",
    "dark": "#3A2F17"
  },
  "--dsw-alias-state-warn-label": {
    "light": "#8A6319",
    "dark": "#D9A94F"
  },
  "--dsw-alias-switch-thumb": {
    "light": "#FFFEFA",
    "dark": "#A6B0A0"
  },
  "--dsw-alias-toast-bg": {
    "light": "#2E332E",
    "dark": "#DCE1D4"
  },
  "--dsw-alias-toast-label": {
    "light": "#F6F4ED",
    "dark": "#22301F"
  },
  "--dsw-alias-tooltip-bg": {
    "light": "#2E332E",
    "dark": "#223129"
  },
  "--dsw-alias-tooltip-key-bg": {
    "light": "#474D46",
    "dark": "#35443A"
  },
  "--dsw-alias-code-diff-added": {
    "light": "#33684A14",
    "dark": "#83BB971F"
  },
  "--dsw-alias-code-diff-deleted": {
    "light": "#B0392C14",
    "dark": "#E0826D1F"
  },
  "--dsw-alias-file-diff-added-bg": {
    "light": "#E7EFE3",
    "dark": "#22352A"
  },
  "--dsw-alias-file-diff-added-gutter": {
    "light": "#EDF3EA",
    "dark": "#182720"
  },
  "--dsw-alias-file-diff-added-marker": {
    "light": "#33684A",
    "dark": "#83BB97"
  },
  "--dsw-alias-file-diff-deleted-bg": {
    "light": "#F5E4DE",
    "dark": "#3A241F"
  },
  "--dsw-alias-file-diff-deleted-gutter": {
    "light": "#F8ECE7",
    "dark": "#291A16"
  },
  "--dsw-alias-file-diff-deleted-marker": {
    "light": "#B0392C",
    "dark": "#E68F7B"
  },
  "--dsw-specific-bubble": {
    "light": "#F2E6DC",
    "dark": "#35463B"
  },
  "--dsw-specific-bubble-highlight": {
    "light": "#E8D3C3",
    "dark": "#3E5245"
  },
  "--dsw-specific-input-major": {
    "light": "#FFFEFA",
    "dark": "#31453A"
  },
  "--dsw-specific-login-input": {
    "light": "#F1EEE3",
    "dark": "#2A3C31"
  },
  "--dsw-menu-surface-fill": {
    "light": "#FBF9F2F2",
    "dark": "#232F27F2"
  },
  "--dsw-alias-menu-group-header-fill": {
    "light": "#FBF9F2F7",
    "dark": "#1E2820F7"
  },
  "--dsw-specific-menu": {
    "light": "#FBF9F2F2",
    "dark": "#232F27F2"
  },
  "--dsw-specific-selector": {
    "light": "#F1EEE3",
    "dark": "#3A4E42"
  },
  "--dsw-specific-sidebar-fill": {
    "light": "#F1EEE4",
    "dark": "#243529"
  },
  "--dsw-specific-sidebar-nav-item-active": {
    "light": "#E9E4D6",
    "dark": "#33493C"
  },
  "--dsw-specific-sidebar-nav-item-active-accent": {
    "light": "#F0DCCE",
    "dark": "#4A5F51"
  },
  "--dsw-specific-sidebar-nav-item-hover": {
    "light": "#EDE9DD",
    "dark": "#2E4136"
  },
  "--dsw-specific-tip": {
    "light": "#F1EEE3",
    "dark": "#3A4E42"
  },
  "--dsw-alias-turn-trigger-bg": {
    "light": "#F0EDE2",
    "dark": "#F6F4ED14"
  },
  "--dsw-alias-turn-trigger-bg-hover": {
    "light": "#252A260F",
    "dark": "#F6F4ED24"
  },
  "--dsw-alias-onboarding-accent": {
    "light": "#B86146",
    "dark": "#C9805F"
  },
  "--dsw-gradient-onboarding-violet-stops": {
    "light": "#9E4E33 33.102%, #C9805F 50.954%, #E9D5C9 85.326%, #9E4E33",
    "dark": "#9E4E33 33.102%, #C9805F 50.954%, #E9D5C9 85.326%, #9E4E33"
  },
  "--dsw-gradient-onboarding-blue-stops": {
    "light": "#293D32 18.75%, #3A5C48 51.78%, #7FA98E 86.252%, #293D32",
    "dark": "#293D32 18.75%, #3A5C48 51.78%, #7FA98E 86.252%, #293D32"
  },
  "--dsw-gradient-onboarding-cyan-stops": {
    "light": "#B86146 21.154%, #D9A08A 50.954%, #F2E3D5 85.326%, #B86146",
    "dark": "#B86146 21.154%, #D9A08A 50.954%, #F2E3D5 85.326%, #B86146"
  },
  "--dsw-alias-onboarding-card-fill": {
    "light": "color-mix(in srgb, #FFFEFA 80%, transparent)",
    "dark": "color-mix(in srgb, #26332A 80%, transparent)"
  },
  "--dsw-alias-onboarding-secondary-fill": {
    "light": "#FFFEFA",
    "dark": "#44584B"
  },
  "--dsw-alias-onboarding-checkbox-border": {
    "light": "#252A2633",
    "dark": "#F6F4ED33"
  },
  "--dsw-font-family-brand": {
    "light": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif",
    "dark": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif"
  },
  "--dsw-font-markdown-h1-font-family": {
    "light": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif",
    "dark": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif"
  },
  "--dsw-font-markdown-h2-font-family": {
    "light": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif",
    "dark": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif"
  },
  "--dsw-font-xl-24-font-family": {
    "light": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif",
    "dark": "\"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif"
  },
  "--dsw-font-markdown-h1": {
    "light": "700 calc(21px + var(--dsh-content-font-delta)) / calc(34px + var(--dsh-content-font-delta)) \"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif",
    "dark": "700 calc(21px + var(--dsh-content-font-delta)) / calc(34px + var(--dsh-content-font-delta)) \"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif"
  },
  "--dsw-font-markdown-h1-line-height": {
    "light": "calc(34px + var(--dsh-content-font-delta))",
    "dark": "calc(34px + var(--dsh-content-font-delta))"
  },
  "--dsw-font-markdown-h2": {
    "light": "700 calc(19px + var(--dsh-content-font-delta)) / calc(31px + var(--dsh-content-font-delta)) \"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif",
    "dark": "700 calc(19px + var(--dsh-content-font-delta)) / calc(31px + var(--dsh-content-font-delta)) \"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif"
  },
  "--dsw-font-markdown-h2-line-height": {
    "light": "calc(31px + var(--dsh-content-font-delta))",
    "dark": "calc(31px + var(--dsh-content-font-delta))"
  },
  "--dsw-font-xl-24": {
    "light": "600 24px/34px \"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif",
    "dark": "600 24px/34px \"Georgia\",\"Noto Serif SC\",\"Source Han Serif SC\",\"思源宋体\",\"STZhongsong\",\"SimSun\",serif"
  },
  "--ds-ease-in-out": {
    "light": "cubic-bezier(0.25, 0.1, 0.25, 1)",
    "dark": "cubic-bezier(0.25, 0.1, 0.25, 1)"
  },
  "--ds-transition-duration": {
    "light": "0.22s",
    "dark": "0.22s"
  },
  "--ds-transition-duration-fast": {
    "light": "0.12s",
    "dark": "0.12s"
  },
  "--ds-transition-duration-slow": {
    "light": "0.32s",
    "dark": "0.32s"
  }
};
    var CALM_CSS = "/* Karlo Calm - material layer: warm soft shadows, paper menus, quiet selection. On paper,\nsurfaces separate by tone step; floating layers carry shadow only, no hairline rings. */\nbody{\n  --dsw-shadow-lv1:0 1px 2px rgba(46,38,26,.05), 0 1px 3px rgba(46,38,26,.04);\n  --dsw-shadow-lv1-blur:0 4px 12px rgba(46,38,26,.04);\n  --dsw-shadow-lv2:0 1px 3px rgba(46,38,26,.05), 0 4px 12px rgba(46,38,26,.05);\n  --dsw-shadow-lv3:0 0 1px rgba(46,38,26,.12), 0 12px 32px rgba(46,38,26,.10); /* taste-skill-ignore: token value for the harness's own dialogs */\n  --dsw-menu-backdrop-filter:blur(20px) saturate(120%); /* taste-skill-ignore: token value for the harness's own menus */\n  --dsw-linear-gradient-think:linear-gradient(180deg, #F6F4ED 20.19%, #F6F4ED00 100%); /* taste-skill-ignore: token value for the harness's own thinking fade */\n  --dsw-linear-think-select:linear-gradient(180deg, #EFECE1 20.19%, #EFECE100 100%); /* taste-skill-ignore: token value for the harness's own thinking fade */\n}\nbody, body *{\n  --dsw-elevation-panel:0 2px 6px rgba(46,38,26,.05), 0 0 12px rgba(46,38,26,.03);\n  --dsw-elevation-prominent:0 1px 3px rgba(46,38,26,.06), 0 4px 12px rgba(46,38,26,.08);\n  --dsw-elevation-soft:0 4px 16px rgba(46,38,26,.06), 0 0 20px rgba(46,38,26,.04);\n}\nbody[data-ds-dark-theme]{\n  --dsw-shadow-lv1:0 1px 2px rgba(0,0,0,.20), 0 1px 3px rgba(0,0,0,.16);\n  --dsw-shadow-lv1-blur:0 4px 12px rgba(0,0,0,.14);\n  --dsw-shadow-lv2:0 1px 3px rgba(0,0,0,.20), 0 4px 12px rgba(0,0,0,.16);\n  --dsw-shadow-lv3:0 0 1px rgba(0,0,0,.40), 0 12px 32px rgba(0,0,0,.30); /* taste-skill-ignore: token value for the harness's own dialogs */\n  --dsw-linear-gradient-think:linear-gradient(180deg, #223129 20.19%, #22312900 100%); /* taste-skill-ignore: token value for the harness's own thinking fade */\n  --dsw-linear-think-select:linear-gradient(180deg, #2C3F33 20.19%, #2C3F3300 100%); /* taste-skill-ignore: token value for the harness's own thinking fade */\n}\nbody[data-ds-dark-theme], body[data-ds-dark-theme] *{\n  --dsw-elevation-panel:0 2px 8px rgba(0,0,0,.22);\n  --dsw-elevation-prominent:0 1px 3px rgba(0,0,0,.3), 0 4px 12px rgba(0,0,0,.30);\n  --dsw-elevation-soft:0 6px 20px rgba(0,0,0,.26);\n}\nbody ::selection{background-color:#B8614633}\nbody[data-ds-dark-theme] ::selection{background-color:#C9805F4D}\n";
    return {
      inject: ['theme'],
      apply(ctx) {
        ctx.effect(
          () => ctx.theme.overrideTokens("@local/karlo-calm", TOKENS),
          'karlo-calm: KARLO alias-token palette layer'
        );
        ctx.effect(() => {
          if (typeof document === 'undefined') return undefined;
          var tag = document.createElement('style');
          tag.dataset.plugin = "@local/karlo-calm";
          tag.dataset.pluginCss = "@local/karlo-calm/calm.css";
          tag.textContent = CALM_CSS;
          document.head.appendChild(tag);
          return function () { tag.remove(); };
        }, 'karlo-calm: calm material stylesheet');
      },
    };
  },
});
