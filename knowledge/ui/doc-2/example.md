```yaml
# tokens.yaml — 设计令牌定义
global:
  color:
    gray-50: { value: "#FAFAFA", type: "color" }
    gray-100: { value: "#F5F5F5", type: "color" }
    gray-900: { value: "#262626", type: "color" }
    blue-500: { value: "#1890FF", type: "color" }
    red-500: { value: "#FF4D4F", type: "color" }
    green-500: { value: "#52C41A", type: "color" }

alias:
  color:
    brand: { value: "{blue-500}", type: "color" }
    success: { value: "{green-500}", type: "color" }
    error: { value: "{red-500}", type: "color" }
    text-primary: { value: "{gray-900}", type: "color" }
    text-secondary: { value: "{gray-500}", type: "color" }
    bg-primary: { value: "{gray-50}", type: "color" }

component:
  button:
    primary-bg: { value: "{color.brand}", type: "color" }
    primary-hover-bg: { value: "{blue-400}", type: "color" }
    padding-x: { value: "16px", type: "dimension" }
    padding-y: { value: "8px", type: "dimension" }
```