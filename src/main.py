from pipeline import NeurolabsPipeline
import sys, os
sys.path.append(os.path.dirname(__file__))


if __name__ == "__main__":
    pipeline = NeurolabsPipeline()
    pipeline.run_full_pipeline()
