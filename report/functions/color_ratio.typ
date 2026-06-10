
// This function was entirely written by Gemini
#let color-ratio(ratio-str) = {
  // 1. Split the string by the slash
  let parts = ratio-str.split("/")
  
  if parts.len() != 2 {
    return [Invalid ratio]
  }
  
  // 2. Convert the string parts to floats
  let num = float(parts.at(0))
  let den = float(parts.at(1))
  
  // Prevent division by zero
  if den == 0 { return text(fill: rgb("ff0000"))[#ratio-str] }
  
  // 3. Calculate the ratio (clamped between 0 and 1)
  let val = calc.min(calc.max(num / den, 0.0), 1.0)
  
  // 4. Create a 3-stop gradient and sample from it using a percentage
  let grad = gradient.linear(red, yellow, rgb("00aa00"))
  let target-color = grad.sample(val * 100%)
  
  // 5. Return the styled text
  text(fill: target-color, weight: "bold")[#ratio-str]
}

#let color-latency(latency-str) = {
  let val = float(latency-str)
  val = val / 16.0
  let grad = gradient.linear(..color.map.flare)
  let target-color = grad.sample(val * 100%)
  text(fill: target-color, weight: "bold")[#latency-str]
}

