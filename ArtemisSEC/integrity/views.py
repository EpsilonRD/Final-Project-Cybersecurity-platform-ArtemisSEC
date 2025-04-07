from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import hashlib
from .models import IntegrityCheck
# Create your views here.

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import hashlib
from .models import IntegrityCheck

def calculate_hash(file, algorithm="sha256"):
    """Calcula el hash de un archivo usando el algoritmo especificado."""
    hash_functions = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha384": hashlib.sha384,
        "sha512": hashlib.sha512,
    }
    
    algorithm = algorithm.lower()
    if algorithm not in hash_functions:
        raise ValueError(f"Unsupported algorithm: {algorithm}. Supported: {', '.join(hash_functions.keys())}")
    
    hash_obj = hash_functions[algorithm]()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_obj.update(chunk)
    file.seek(0)
    return hash_obj.hexdigest()

class IntegrityCheckView(View):
    template_name = "integrity/integrity.html"

    def get(self, request, *args, **kwargs):
        """Muestra el formulario vacío o carga un resultado desde el historial."""
        check_id = request.GET.get("check_id")
        if check_id:
            try:
                check = IntegrityCheck.objects.get(id=check_id)
                if check.is_valid:
                    result = "The file is intact. Hashes match."
                else:
                    result = f"The file is not intact.\nCalculated hash: {check.calculated_hash}\nExpected hash: {check.reference_hash}"
                return render(request, self.template_name, {"result": result})
            except IntegrityCheck.DoesNotExist:
                return render(request, self.template_name, {"result": "Error: Check not found."})
        return render(request, self.template_name, {"result": None})

    def post(self, request, *args, **kwargs):
        """Procesa el formulario enviado y guarda el resultado en el historial."""
        file = request.FILES.get("file")
        reference_hash = request.POST.get("reference_hash", "").strip().lower()
        algorithm = request.POST.get("algorithm", "sha256")

        if not file or not reference_hash:
            return render(request, self.template_name, {
                "result": "Error: You must upload a file and provide a hash."
            })

        valid_algorithms = ["md5", "sha1", "sha256", "sha384", "sha512"]
        if algorithm not in valid_algorithms:
            return render(request, self.template_name, {
                "result": f"Error: Unsupported algorithm. Use one of: {', '.join(valid_algorithms)}."
            })

        try:
            calculated_hash = calculate_hash(file, algorithm)
            is_valid = calculated_hash == reference_hash

            # Guardar en el historial
            check = IntegrityCheck.objects.create(
                file_name=file.name,
                calculated_hash=calculated_hash,
                reference_hash=reference_hash,
                algorithm=algorithm,
                timestamp=timezone.now(),
                is_valid=is_valid
            )

            # Preparar el resultado
            if is_valid:
                result = "The file is intact. Hashes match."
            else:
                result = f"The file is not intact.\nCalculated hash: {calculated_hash}\nExpected hash: {reference_hash}"

            return render(request, self.template_name, {"result": result})

        except ValueError as e:
            return render(request, self.template_name, {"result": str(e)})
        except Exception as e:
            return render(request, self.template_name, {"result": f"An unexpected error occurred: {str(e)}"})

class IntegrityHistoryView(View):
    def get(self, request, *args, **kwargs):
        """Devuelve el historial de verificaciones en formato JSON."""
        history = IntegrityCheck.objects.all().order_by('-timestamp')[:10]
        history_data = [
            {
                "id": check.id,  # Añadimos el ID para el enlace
                "file_name": check.file_name,
                "calculated_hash": check.calculated_hash,
                "reference_hash": check.reference_hash,
                "algorithm": check.algorithm,
                "timestamp": check.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "is_valid": check.is_valid
            }
            for check in history
        ]
        return JsonResponse({"history": history_data})