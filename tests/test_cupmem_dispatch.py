import unittest
from evaluation.cupmem.dispatch import validate_submission
from evaluation.timeline.dispatch import scheduler_max_policy


class SubmissionPolicy(unittest.TestCase):
    def test_account_maximum_replaces_manual_caps_but_enforces_walltime(self):
        policy=dict(mode='scheduler_account_maximum',authorized_by_user=True,
            enforce_cumulative_gpu_caps=False,max_wall_minutes=8640,
            max_wall='6-00:00:00',qos='qos_pjw031003_2026_2')
        data=dict(execution_time_policy=policy)
        script='#SBATCH --qos=qos_pjw031003_2026_2\n#SBATCH --time=6-00:00:00\n'
        self.assertEqual(scheduler_max_policy(data,8640,script),policy)
        with self.assertRaises(RuntimeError):scheduler_max_policy(data,45,script)
        with self.assertRaises(RuntimeError):scheduler_max_policy(data,8640,script.replace('6-00:00:00','00:45:00'))
        self.assertIsNone(scheduler_max_policy({},45,''))
        policy.update(mode='fixed_walltime',wall_minutes=720,walltime='12:00:00')
        self.assertEqual(scheduler_max_policy(data,720,script.replace('6-00:00:00','12:00:00')),policy)
        with self.assertRaises(RuntimeError):scheduler_max_policy(data,8640,script)

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
