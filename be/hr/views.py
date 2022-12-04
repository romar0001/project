from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from django.db import transaction


from users.permissions import HROnly
from .serializers import (
    EvaluationRubricSerializer,
    EmployeeEvaluationSerializer,
    EvaluationRubric,
    EmployeeEvaluation,
    EmployeeEvaluationDetail,
    Sales,
    SalesSerializer,
)
from users.serializers import (
    UserSerializer,
    User,
)


class EvalutationRubricView(GenericViewSet):   
    permission_classes = (HROnly,)
    serializer_class = EvaluationRubricSerializer

    def get_queryset(self):
        queryset = EvaluationRubric.objects.all()
        print(queryset)
        type = self.request.query_params.get('emptype')
        if type is not None:
            queryset = queryset.filter(employee_type=type)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    # def list(self, request,):
    #     data = EvaluationRubric.objects.all()
    #     serializer = EvaluationRubricSerializer(data, many=True)
    #     return Response(serializer.data , status=status.HTTP_200_OK)

    def listCore(self, request,):
        data = self.get_queryset().filter(type = 'CORE')
        serializer = EvaluationRubricSerializer(data, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


    def listKpi(self, request, **kwargs):
        data = self.get_queryset().filter(type = 'KPI')
        serializer = EvaluationRubricSerializer(data, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        rubric = EvaluationRubric.objects.get(id=kwargs['pk'])
        data = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rubric.name = data.get("name", rubric.name)
        rubric.description = data.get("description", rubric.description)
        rubric.type = data.get("type", rubric.type)
        rubric.employee_type = data.get("employee_type", rubric.employee_type)
        rubric.percentage = data.get("percentage", rubric.percentage)

        
        rubric.save()
        
        return Response(serializer.data,  status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        rubric = EvaluationRubric.objects.get(id=kwargs['pk'])
        if rubric.editable is True:
            rubric.delete()
            return Response('Rubric Deleted',  status=status.HTTP_200_OK)
        else:
            return Response('You are not allowed to delete this Rubric',  status=status.HTTP_200_OK)
        


class EmployeeEvaluationView(GenericViewSet):
    serializer_class = EmployeeEvaluationSerializer
    queryset = EmployeeEvaluation.objects.all()

    def list(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        evaluation_serializer = ''
        
        user_serializer = UserSerializer(user, many=False)

        rubrics = ''
        if 'id' in kwargs.keys():
            evaluation_serializer = self.serializer_class(
            self.get_queryset().get(id=kwargs['id']), many=False)
        else:
            evaluation_serializer = self.serializer_class(
            self.get_queryset().filter(employee=user).order_by('-date_created'), many=True)


        return Response({
            'evaluation_list': evaluation_serializer.data,
            'user': user_serializer.data
        },status=status.HTTP_200_OK)



class SalesView(GenericViewSet):
    serializer_class = SalesSerializer
    queryset = Sales.objects.all()

    def list(self, request, *args, **kwargs):

        return Response(status=status.HTTP_200_OK)
    

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['userId'])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(status=status.HTTP_200_OK)