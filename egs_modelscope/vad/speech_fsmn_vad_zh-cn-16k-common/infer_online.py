from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import soundfile


if __name__ == '__main__':
    output_dir = None
    inference_pipline = pipeline(
        task=Tasks.voice_activity_detection,
        model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        model_revision='v1.1.9',
        output_dir=None,
        batch_size=1,
    )
    speech, sample_rate = soundfile.read("./vad_example_16k.wav")
    speech_length = speech.shape[0]
    
    sample_offset = 0
    
    step = 160 * 10
    param_dict = {'in_cache': dict()}
    for sample_offset in range(0, speech_length, min(step, speech_length - sample_offset)):
        if sample_offset + step >= speech_length - 1:
            step = speech_length - sample_offset
            is_final = True
        else:
            is_final = False
        param_dict['is_final'] = is_final
        segments_result = inference_pipline(audio_in=speech[sample_offset: sample_offset + step],
                                            param_dict=param_dict)
        print(segments_result)

