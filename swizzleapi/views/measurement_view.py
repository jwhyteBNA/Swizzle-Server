from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from swizzleapi.models import Measurement

class MeasurementView(ViewSet):

    def retrieve(self, request, pk):
        """Get a single ingredient"""
        try:
            measurement = Measurement.objects.get(pk=pk)
            serializer = MeasurementSerializer(measurement)
            return Response(serializer.data)
        except Measurement.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get a list of all ingredients"""
        measurements = Measurement.objects.all()

        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Create a new measurement for use"""
        try:
            measurement = Measurement.objects.create(
                unit_short=request.data['unit_short'],
                unit_long=request.data['unit_long'],
                unit_plural=request.data['unit_plural'],
            )
            serializer = MeasurementSerializer(measurement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Update a measurement"""
        measurement = Measurement.objects.get(pk=pk)

        measurement.unit_short = request.data['unit_short'],
        measurement.unit_long = request.data['unit_long'],
        measurement.unit_plural = request.data['unit_plural']
        measurement.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete a measurement"""
        try:
            Measurement = Measurement.objects.get(pk=pk)
            Measurement.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Measurement.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'unit_short', 'unit_long', 'unit_plural')
        depth = 1
