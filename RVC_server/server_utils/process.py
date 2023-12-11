import io
from google.cloud import speech


# google stt로 음성을 텍스트로 바꿔 반환하는 함수
def SST(speech_client, segment):
    # 버퍼에서 오디오 데이터 읽기
    audio = speech.RecognitionAudio(content=segment)

    # 음성 인식 설정
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="ko-KR",
    )

    # 구글 클라우드 스피치 API 호출
    response = speech_client.recognize(config=config, audio=audio)

    # 결과들을 텍스트로 결합
    transcripts = [result.alternatives[0].transcript for result in response.results]
    combined_transcript = " ".join(transcripts)

    return combined_transcript


# 세그먼트를 구글 클라우드 스토리지에 저장하는 함수
def save_segment_to_gcs(bucket, speech_client, segment, GCS_index):
    # 메모리 상의 io.BytesIO 스트림에 세그먼트 저장
    buffer = io.BytesIO()
    segment.export(buffer, format="wav")
    SST_result = SST(speech_client, buffer.getvalue())
    buffer.seek(0)  # 스트림을 처음으로 되돌림

    # 파일명 생성 (예: segment_1.wav)
    segment_name = f"{GCS_index}_{SST_result}"

    # 구글 클라우드 스토리지에 업로드
    blob = bucket.blob(segment_name)
    blob.upload_from_file(buffer, content_type="audio/wav")

    # 필요한 경우, 데이터베이스에 세그먼트 정보 저장
    # 예: database.save(segment_info)
    return
