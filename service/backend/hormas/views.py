# 이 파일의 내용을 아래 코드로 완전히 교체하세요.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# 1. FormParser와 MultiPartParser를 추가로 임포트합니다.
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from nlp_model.model.model import ReviewResponder
from django.utils import timezone

from .serializers import (
    RaraModelSerializer,
    CustomRaraModelSerializer,
    RaraRatingSerializer,
    RaraSurveySerializer,
)
from .models import RaraModel, RaraSurveyModel

# Create your views here.

API_KEY = "sk-your-api-key-here" 

class RaraModelView(APIView):
    permission_classes = (AllowAny,)
    # 2. 파서 목록에 FormParser와 MultiPartParser를 추가합니다.
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = RaraModelSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.validated_data.get("model")
            inputText = serializer.validated_data.get("inputText")
            response_method = serializer.validated_data.get("response_method")
            analysis_model = serializer.validated_data.get("analysis_model")
            time = timezone.now()

            if response_method == "basic":
                basic_responder = ReviewResponder(
                    API_KEY, model_name=model, analysis_model_name=analysis_model
                )
                result = basic_responder.Response(inputText)

            if response_method == "normal":
                normal_responder = ReviewResponder(API_KEY, model_name=model)
                result = normal_responder.Response(inputText, method="normal")

            if response_method == "nocot":
                nocot_responder = ReviewResponder(
                    API_KEY,
                    model_name=model,
                    nocot=True,
                    analysis_model_name=analysis_model,
                )
                result = nocot_responder.Response(inputText)

            instance = RaraModel.objects.create(
                model=model,
                analysis_model=analysis_model,
                inputText=inputText,
                response_method=response_method,
                response=result,
                time=time,
            )
            return Response({"response": result})

        return Response(serializer.errors, status=400)

class CustomRaraModelView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        # 1. 요청이 뷰에 도달했는지 확인
        print("\n--- [DEBUG] CustomRaraModelView: POST request received ---")

        # 2. 파서가 데이터를 어떻게 해석했는지 확인
        print(f"[DEBUG] Request data from parser: {request.data}")

        # 3. Serializer에 데이터 전달
        print("[DEBUG] Initializing CustomRaraModelSerializer...")
        serializer = CustomRaraModelSerializer(data=request.data)

        # 4. 유효성 검사 시도
        print("[DEBUG] Calling serializer.is_valid()...")
        if serializer.is_valid():
            # 5. 유효성 검사 통과 시
            print("[DEBUG] Serializer is VALID.")
            print(f"[DEBUG] Validated data: {serializer.validated_data}")

            model = serializer.validated_data.get("model")
            analysis_model = serializer.validated_data.get("analysis_model")
            responder_name = serializer.validated_data.get("responder_name")
            contact = serializer.validated_data.get("contact")
            rag_list_str = serializer.validated_data.get("retrieval", "")
            rag = bool(rag_list_str)
            rag_list = rag_list_str.split("\n") if rag_list_str else []
            time = timezone.now()
            response_method = serializer.validated_data.get("response_method")
            
            print(f"[DEBUG] Processing with response_method: '{response_method}'")

            if response_method == "custom":
                print("[DEBUG] Executing 'custom' logic branch...")
                custom_responder = ReviewResponder(
                    api_key=API_KEY,
                    responder_name=responder_name,
                    contact=contact,
                    rag=rag,
                    rag_list=rag_list,
                    analysis_model_name=analysis_model,
                    model_name=model,
                )
                inputText = serializer.validated_data.get("inputText")
                result = custom_responder.Response(inputText)

                # ... (DB 저장 로직) ...
                print("[DEBUG] 'custom' branch finished. Sending response.")
                return Response({"response": result})
            
            if response_method == "final":
                print("[DEBUG] Executing 'final' logic branch...")
                normal_responder = ReviewResponder(
                    api_key=API_KEY, 
                    model_name=model)
                custom_responder = ReviewResponder(
                    api_key=API_KEY,
                    responder_name=responder_name,
                    contact=contact,
                    rag=rag,
                    rag_list=rag_list,
                    analysis_model_name=analysis_model,
                    model_name=model,
                )
                inputText = serializer.validated_data.get("inputText")
                norm_response = normal_responder.Response(inputText, method="normal")
                result = custom_responder.Response(inputText, "final")
                
                print(f"[DEBUG] Normal Response: {norm_response}")
                print(f"[DEBUG] HormAS Response: {result}")
                
                # ... (DB 저장 로직) ...
                print("[DEBUG] 'final' branch finished. Sending response.")
                return Response({"response": result, "norm": norm_response})
            
            if response_method == "multi":
                print("[DEBUG] Executing 'multi' logic branch...")
                custom_responder = ReviewResponder(
                    api_key=API_KEY,
                    responder_name=responder_name,
                    contact=contact,
                    rag=rag,
                    rag_list=rag_list,
                    analysis_model_name=analysis_model,
                    model_name=model,
                )
                inputText = serializer.validated_data.get("inputText")
                result = custom_responder.Response(inputText, "final")
                
                print(f"[DEBUG] HormAS Response: {result}")
                
                # ... (DB 저장 로직) ...
                print("[DEBUG] 'multi' branch finished. Sending response.")
                return Response({"response": result})
        
        # 6. 유효성 검사 실패 시
        print("[DEBUG] Serializer is NOT VALID.")
        # 7. 실패 원인(에러)을 상세하게 출력 (가장 중요!)
        print(f"[DEBUG] Serializer errors: {serializer.errors}")
        print("[DEBUG] Sending 400 Bad Request response.")
        return Response(serializer.errors, status=400)


class RaraRatingView(APIView):
    permission_classes = (AllowAny,)
    # 2. 파서 목록에 FormParser와 MultiPartParser를 추가합니다.
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = RaraRatingSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.validated_data.get("model")
            inputText = serializer.validated_data.get("inputText")
            response = serializer.validated_data.get("response")
            response_method = serializer.validated_data.get("response_method")
            analysis_model = serializer.validated_data.get("analysis_model")
            user_rating = serializer.validated_data.get("user_rating")

            try:
                instance = RaraModel.objects.get(
                    model=model,
                    inputText=inputText,
                    response=response,
                    response_method=response_method,
                    analysis_model=analysis_model,
                )

                instance.user_rating = user_rating
                instance.save()

                return Response({"Success"}, status=200)

            except Exception as e:
                print(f"Database Error occur: {e}")
                return Response(serializer.errors, status=400)

        return Response(serializer.errors, status=400)


class RaraSurveyView(APIView):
    permission_classes = (AllowAny,)
    # 2. 파서 목록에 FormParser와 MultiPartParser를 추가합니다.
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = RaraSurveySerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            organization = serializer.validated_data.get("organization")
            contact = serializer.validated_data.get("contact")
            email = serializer.validated_data.get("email")
            dataidx = serializer.validated_data.get("dataidx")
            select_value = serializer.validated_data.get("select_value")
            time = timezone.now()

            instance = RaraSurveyModel.objects.create(
                name=name,
                organization=organization,
                contact=contact,
                email=email,
                dataidx=dataidx,
                select_value=select_value,
                time=time,
            )

            return Response({"Success"}, status=200)

        return Response(serializer.errors, status=400)