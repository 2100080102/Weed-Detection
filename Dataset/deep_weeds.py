import csv
import os
import tensorflow as tf
import tensorflow_datasets as tfds

_LOCAL_ZIP_PATH = "D:\\Users\\acer\\PycharmProjects\\WeedDetection\\Manual_download\\images.zip"
_URL_LABELS = "https://raw.githubusercontent.com/AlexOlsen/DeepWeeds/master/labels/labels.csv"

_DESCRIPTION = (
    "The DeepWeeds dataset consists of 17,509 images capturing eight different weed species native to Australia "
    "in situ with neighbouring flora. The selected weed species are local to pastoral grasslands across the state of Queensland. "
    "The images were collected from weed infestations at the following sites across Queensland: Black River, Charters Towers, "
    "Cluden, Douglas, Hervey Range, Kelso, McKinlay, and Paluma."
)

_IMAGE_SHAPE = (256, 256, 3)

_CITATION = """\
@article{DeepWeeds2019,
  author = {Alex Olsen and
    Dmitry A. Konovalov and
    Bronson Philippa and
    Peter Ridd and
    Jake C. Wood and
    Jamie Johns and
    Wesley Banks and
    Benjamin Girgenti and
    Owen Kenny and
    James Whinney and
    Brendan Calvert and
    Mostafa {Rahimi Azghadi} and
    Ronald D. White},
  title = {{DeepWeeds: A Multiclass Weed Species Image Dataset for Deep Learning}},
  journal = {Scientific Reports},
  year = 2019,
  number = 2058,
  month = 2,
  volume = 9,
  issue = 1,
  day = 14,
  url = "https://doi.org/10.1038/s41598-018-38343-3",
  doi = "10.1038/s41598-018-38343-3"
}
"""

class DeepWeeds(tfds.core.GeneratorBasedBuilder):
    """DeepWeeds Image Dataset Class."""

    VERSION = tfds.core.Version("3.0.0")
    RELEASE_NOTES = {
        "3.0.0": "Update download URL.",
        "2.0.0": "Fixes wrong labels in V1.",
    }

    def _info(self):
        """Define Dataset Info."""
        return tfds.core.DatasetInfo(
            builder=self,
            description=_DESCRIPTION,
            features=tfds.features.FeaturesDict({
                "image": tfds.features.Image(shape=_IMAGE_SHAPE),
                "label": tfds.features.ClassLabel(num_classes=9),
            }),
            supervised_keys=("image", "label"),
            homepage="https://github.com/AlexOlsen/DeepWeeds",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Define Splits."""
        # Ensure that the local zip file exists
        if not tf.io.gfile.exists(_LOCAL_ZIP_PATH):
            raise FileNotFoundError(f"{_LOCAL_ZIP_PATH} does not exist. Please download the dataset manually.")

        # Use the local file directly
        paths = {
            "image": dl_manager.extract(_LOCAL_ZIP_PATH),
            "label": dl_manager.download_and_extract(_URL_LABELS),
        }

        return [
            tfds.core.SplitGenerator(
                name="train",
                gen_kwargs={
                    "data_dir_path": paths["image"],
                    "label_path": paths["label"],
                },
            ),
        ]

    def _generate_examples(self, data_dir_path, label_path):
        """Generate images and labels for splits."""
        with tf.io.gfile.GFile(label_path, 'r') as f:
            reader = list(csv.DictReader(f))

        label_id_to_name = {int(row["Label"]): row["Species"] for row in reader}
        self.info.features["label"].names = [v for _, v in sorted(label_id_to_name.items())]

        filename_to_label = {row["Filename"]: row["Species"] for row in reader}
        for file_name in tf.io.gfile.listdir(data_dir_path):
            yield file_name, {
                "image": os.path.join(data_dir_path, file_name),
                "label": filename_to_label.get(file_name),
            }
