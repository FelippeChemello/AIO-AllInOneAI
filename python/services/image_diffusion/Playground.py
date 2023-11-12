import asyncio
import random
import requests
import os
from fastapi.responses import JSONResponse

class Playground:
    def __init__(self):
        super().__init__()
        self.image_cache = {}
        self.generating_images = {}

    async def generate_image(self, prompt):
        if prompt in self.image_cache:
            image = self.image_cache[prompt]
            return image

        async with self.generating_images.get(prompt, asyncio.Lock()):
            if prompt in self.image_cache:
                image = self.image_cache[prompt]
                return image

            future = asyncio.Future()
            self.generating_images[prompt] = future

            try:
                image = await self.generate_image_async(prompt)

                self.image_cache[prompt] = image
                future.set_result(image)

                return image
            except Exception as e:
                return JSONResponse(content={"error": str(e)}, status_code=500)
            finally:
                del self.generating_images[prompt]

    async def generate_image_async(self, prompt):
        payload = {
            "width": 1024,
            "height": 1024,
            "seed": random.randint(1, 1000000000),
            "num_images": 1,
            "sampler": 1,
            "cfg_scale": 7,
            "guidance_scale": 7,
            "strength": 1.3,
            "steps": 30,
            "negativePrompt": 'out of frame, lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature,',
            "prompt": prompt,
            "hide": False,
            "isPrivate": False,
            "modelType": 'stable-diffusion-xl',
            "batchId": 'Jt9pHfw6BL',
            "generateVariants": False,
            "initImageFromPlayground": False
        }

        headers = {
            'Cookie': os.getenv("PLAYGROUND_AI_COOKIES")
        }

        response = requests.post('https://playgroundai.com/api/models', json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            image_url = data['images'][0]['url']
            print("Image URL:", image_url[:100])
            return image_url
        else:
            raise Exception(f"Failed to generate image: {response.status_code} - {response.text}")