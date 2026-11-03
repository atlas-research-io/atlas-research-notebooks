import base64, json, os, subprocess, sys, tempfile
from PIL import Image
STYLE = ("Pokemon FireRed Game Boy Advance pixel art, GBA era, bright saturated colors, chunky dark outlines, "
         "flat cel shading with three tones, no gradients, no anti-aliasing, crisp pixels")
NEG = "text, letters, numbers, logo, watermark, blurry, photo, 3d render, gradients, soft shading, painterly, realistic, night, dark, characters, people"
def generate(prompt, seed, out_png):
    body = {"prompt": f"{STYLE}. {prompt}", "negative_prompt": NEG, "mode": "text-to-image", "aspect_ratio": "16:9", "output_format": "png", "seed": seed}
    d = tempfile.mkdtemp(); req, res = os.path.join(d, "req.json"), os.path.join(d, "res.json")
    open(req, "w").write(json.dumps(body))
    subprocess.run(["aws", "bedrock-runtime", "invoke-model", "--region", "us-west-2", "--model-id", "stability.sd3-5-large-v1:0", "--content-type", "application/json", "--accept", "application/json", "--body", f"fileb://{req}", res], check=True, capture_output=True)
    open(out_png, "wb").write(base64.b64decode(json.load(open(res))["images"][0]))
def snap(src, dst, w=320, h=180, colors=48):
    Image.open(src).convert("RGB").resize((w, h), Image.BOX).quantize(colors=colors, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB").save(dst)
if __name__ == "__main__":
    name, seed, prompt = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    outdir = sys.argv[4] if len(sys.argv) > 4 else "."
    raw = os.path.join(outdir, f"{name}-raw.png"); generate(prompt, seed, raw); snap(raw, os.path.join(outdir, f"{name}.png")); print(os.path.join(outdir, f"{name}.png"))
