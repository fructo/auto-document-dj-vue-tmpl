from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm, UserProfileForm, DocumentTemplateForm, create_fill_template_form
from .models import UserProfile, GeneratedDocument, DocumentTemplate
from .utils import extract_tags
from docxtpl import DocxTemplate
import os


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('dashboard')
    else:
        profile_form = UserProfileForm(instance=profile)

    documents = GeneratedDocument.objects.filter(user=request.user).order_by('-created_at')
    templates = DocumentTemplate.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'profile_form': profile_form,
        'documents': documents,
        'templates': templates,
        'document_template_form': DocumentTemplateForm()
    })


@login_required
def generate_acts(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            context = {
                'organization_name': form.cleaned_data['organization_name'],
                'inn': form.cleaned_data['inn'],
                'ogrn': form.cleaned_data['ogrn'],
                'address': form.cleaned_data['address'],
                'responsible_person': form.cleaned_data['responsible_person'],
                'position': form.cleaned_data['position'],
            }
            doc = DocxTemplate("template/template.docx")
            doc.render(context)
            output_path = os.path.join("template/", "generated_acts.docx")
            doc.save(output_path)

            GeneratedDocument.objects.create(
                user=request.user,
                document_type='acts',
                organization_name=form.cleaned_data['organization_name'],
                inn=form.cleaned_data['inn'],
                ogrn=form.cleaned_data['ogrn'],
                address=form.cleaned_data['address'],
                responsible_person=form.cleaned_data['responsible_person'],
                position=form.cleaned_data['position']
            )

            with open(output_path, "rb") as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="generated_acts.docx"'
                return response
    else:
        form = DocumentForm()

    return render(request, 'generate_acts.html', {'form': form})


@login_required
def edit_document(request, document_id):
    document = get_object_or_404(GeneratedDocument, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            context = {
                'organization_name': form.cleaned_data['organization_name'],
                'inn': form.cleaned_data['inn'],
                'ogrn': form.cleaned_data['ogrn'],
                'address': form.cleaned_data['address'],
                'responsible_person': form.cleaned_data['responsible_person'],
                'position': form.cleaned_data['position'],
            }
            document.organization_name = form.cleaned_data['organization_name']
            document.inn = form.cleaned_data['inn']
            document.ogrn = form.cleaned_data['ogrn']
            document.address = form.cleaned_data['address']
            document.responsible_person = form.cleaned_data['responsible_person']
            document.position = form.cleaned_data['position']
            document.save()

            doc = DocxTemplate("template/template.docx")
            doc.render(context)
            output_path = os.path.join("template/", "generated_acts.docx")
            doc.save(output_path)

            with open(output_path, "rb") as f:
                response = HttpResponse(f.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="generated_acts.docx"'
                return response
    else:
        initial_data = {
            'organization_name': document.organization_name,
            'inn': document.inn,
            'ogrn': document.ogrn,
            'address': document.address,
            'responsible_person': document.responsible_person,
            'position': document.position,
        }
        form = DocumentForm(initial=initial_data)

    return render(request, 'edit_document.html', {'form': form, 'document': document})


@login_required
def generate_orders(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            context = {
                'organization_name': form.cleaned_data['organization_name'],
                'inn': form.cleaned_data['inn'],
                'ogrn': form.cleaned_data['ogrn'],
                'responsible_person': form.cleaned_data['responsible_person'],
            }
            doc = DocxTemplate("path/to/orders_template.docx")
            doc.render(context)
            output_path = os.path.join("path/to/save/generated/document", "generated_orders.docx")
            doc.save(output_path)

            # Сохранение информации о сгенерированном документе
            GeneratedDocument.objects.create(
                user=request.user,
                document_type='orders',
                organization_name=form.cleaned_data['organization_name'],
                inn=form.cleaned_data['inn'],
                ogrn=form.cleaned_data['ogrn'],
                responsible_person=form.cleaned_data['responsible_person']
            )

            with open(output_path, "rb") as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="generated_orders.docx"'
                return response
    else:
        form = DocumentForm()

    return render(request, 'generate_orders.html', {'form': form})

@login_required
def generate_document_package(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            context = {
                'organization_name': form.cleaned_data['organization_name'],
                'inn': form.cleaned_data['inn'],
                'ogrn': form.cleaned_data['ogrn'],
                'responsible_person': form.cleaned_data['responsible_person'],
            }
            doc = DocxTemplate("path/to/document_package_template.docx")
            doc.render(context)
            output_path = os.path.join("path/to/save/generated/document", "generated_document_package.docx")
            doc.save(output_path)

            # Сохранение информации о сгенерированном документе
            GeneratedDocument.objects.create(
                user=request.user,
                document_type='document_package',
                organization_name=form.cleaned_data['organization_name'],
                inn=form.cleaned_data['inn'],
                ogrn=form.cleaned_data['ogrn'],
                responsible_person=form.cleaned_data['responsible_person']
            )

            with open(output_path, "rb") as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="generated_document_package.docx"'
                return response
    else:
        form = DocumentForm()

    return render(request, 'generate_document_package.html', {'form': form})

@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

@login_required
def documents(request):
    return render(request, 'documents.html')

@login_required
def tasks(request):
    documents = GeneratedDocument.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks.html', {'documents': documents})

@login_required
def support(request):
    return render(request, 'support.html')

@login_required
def new_request(request):
    if request.method == 'POST':
        form = DocumentTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('dashboard')
    else:
        form = DocumentTemplateForm()

    templates = DocumentTemplate.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'new_request.html', {'form': form, 'templates': templates})


@login_required
def fill_template(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)
    tags = extract_tags(template.template_file.path)
    print("Extracted tags:", tags)  # Отладочное сообщение
    FillTemplateForm = create_fill_template_form(tags)
    if request.method == 'POST':
        form = FillTemplateForm(request.POST)
        if form.is_valid():
            context = {tag: form.cleaned_data[tag] for tag in tags}
            doc = DocxTemplate(template.template_file.path)
            doc.render(context)
            output_path = os.path.join("templates/", f"filled_{template.template_name}.docx")
            doc.save(output_path)

            with open(output_path, "rb") as f:
                response = HttpResponse(f.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename="filled_{template.template_name}.docx"'
                return response
    else:
        form = FillTemplateForm(initial={'template_id': template.id})
        print("Generated form fields:", form.fields)  # Отладочное сообщение

    return render(request, 'fill_template.html', {'form': form, 'template': template})

@login_required
def delete_template(request, template_id):
    template = get_object_or_404(DocumentTemplate, id=template_id)
    if request.method == 'POST':
        template.delete()
        return redirect('dashboard')
    return render(request, 'delete_template.html', {'template': template})
