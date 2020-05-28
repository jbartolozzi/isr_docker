import argparse
import cv2
import tqdm
import os
import pyexr
import numpy as np
from PIL import Image
from ISR.models import RDN, RRDN


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to input directory.")
    parser.add_argument("output", help="Path to output directory.")
    parser.add_argument("-model", type=str, default="gans",
                        choices=["gans", ], help="Image padding around bbox.")
    parser.add_argument("-patch_size", type=int, default=128, help="Image padding around bbox.")
    parser.add_argument("-gpu", "--gpu", type=int,
                        help="Gpu Number.", default=2)

    return parser.parse_args()


def run_video(input_file, output_file, model):

    print("Processing:", input_file)
    video = cv2.VideoCapture(input_file)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    video_file = cv2.VideoWriter(
        filename=os.path.join(output_file),
        fourcc=cv2.VideoWriter_fourcc(*'MP4V'),
        fps=video.get(cv2.CAP_PROP_FPS),
        frameSize=(width * 4, height * 4),
        isColor=True,
    )

    for i in tqdm.trange(num_frames):
        sr_img = model.predict(np.array(video.read()[1]))
        video_file.write(sr_img)
    video_file.release()


def run_exr(input_file, output_file, model):
    result = model.predict(pyexr.read(input_file))
    pyexr.write(output_file, result)


def run_image(input_file, output_file, model):
    sr_img = model.predict(np.array(Image.open(input_file)))
    result = Image.fromarray(sr_img)
    result.save(output_file)

def main():

    args = parse_args()
    input_file = args.input
    output_file = args.output
    model = RRDN(weights="gans")

    if any(t in input_file for t in [".mov", ".mp4", ".mkv"]):
        run_video(input_file, output_file, model)
    elif input_file.endswith(".exr"):
        run_exr(input_file, output_file, model)
    else:
        run_image(input_file, output_file, model)


if __name__ == "__main__":
    main()
