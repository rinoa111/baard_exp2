#!/bin/bash
# chmod +x ./bash/train_3_defence_baard_banknote.sh
# ./bash/train_3_defence_baard_banknote.sh | tee -a ./log/train_3_defence_baard_banknote.log

# banknote
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_apgd_0.2 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_apgd_0.2 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_apgd_0.05 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_apgd_0.05 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_cw2_0.01 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_cw2_0.01 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_cw2_100.0 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_cw2_100.0 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_deepfool_0.001 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_deepfool_0.001 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_deepfool_1e-06 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_deepfool_1e-06 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_fgsm_0.2 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_fgsm_0.2 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_fgsm_0.05 --defence baard --param baard_param_2s.json --suffix 2tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_fgsm_0.05 --defence baard --param baard_param_3s.json --suffix 3tages
python3 ./experiments/train_defences.py --data banknote --pretrained banknote_400.pt --adv banknote_basic16_boundary_0.3 --defence baard --param baard_param_2s.json --suffix 2tages