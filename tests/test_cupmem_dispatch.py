import unittest
from evaluation.cupmem.dispatch import validate_submission


class SubmissionPolicy(unittest.TestCase):
    def test_old_cpu_template_cannot_be_reused_as_gpu_job(self):
        old='#SBATCH --no-requeue\nconda activate /project/env\npython run.py\n'
        for requested in (0,1):
            with self.assertRaises(RuntimeError):validate_submission(old,requested)

    def test_active_conda_gpu_and_scheduler_selected_node(self):
        valid='#SBATCH --gres=gpu:1\n#SBATCH --no-requeue\nconda activate /project/env\npython run.py\n'
        validate_submission(valid,1)
        for bad in (valid.replace('conda activate /project/env',''),valid+'#SBATCH --nodelist=aurora-g8\n',valid.replace('gpu:1','gpu:2')):
            with self.assertRaises(RuntimeError):validate_submission(bad,1)


if __name__=='__main__':unittest.main()
