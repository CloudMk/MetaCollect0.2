// Fonctions générales
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container-fluid').insertBefore(alertDiv, document.querySelector('.container-fluid').firstChild);
}

// Gestion du form builder
class FormBuilder {
    constructor() {
        this.fields = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('addField')?.addEventListener('click', () => this.addField());
        document.getElementById('saveForm')?.addEventListener('click', () => this.saveForm());
    }

    addField(type = 'text') {
        const field = {
            id: Date.now(),
            type: type,
            name: '',
            label: '',
            required: false,
            options: []
        };
        this.fields.push(field);
        this.renderField(field);
    }

    renderField(field) {
        const container = document.getElementById('fields-container');
        const fieldDiv = document.createElement('div');
        fieldDiv.className = 'field-item';
        fieldDiv.id = `field-${field.id}`;
        
        fieldDiv.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <input type="text" class="form-control mb-2" placeholder="Nom du champ" 
                           value="${field.name}" onchange="formBuilder.updateField(${field.id}, 'name', this.value)">
                    <input type="text" class="form-control mb-2" placeholder="Label" 
                           value="${field.label}" onchange="formBuilder.updateField(${field.id}, 'label', this.value)">
                </div>
                <div class="col-md-4">
                    <select class="form-select mb-2" onchange="formBuilder.updateField(${field.id}, 'type', this.value)">
                        <option value="text" ${field.type === 'text' ? 'selected' : ''}>Texte</option>
                        <option value="email" ${field.type === 'email' ? 'selected' : ''}>Email</option>
                        <option value="number" ${field.type === 'number' ? 'selected' : ''}>Nombre</option>
                        <option value="date" ${field.type === 'date' ? 'selected' : ''}>Date</option>
                        <option value="select" ${field.type === 'select' ? 'selected' : ''}>Liste déroulante</option>
                        <option value="textarea" ${field.type === 'textarea' ? 'selected' : ''}>Texte long</option>
                    </select>
                    <div class="form-check">
                        <input type="checkbox" class="form-check-input" id="required-${field.id}" 
                               ${field.required ? 'checked' : ''} 
                               onchange="formBuilder.updateField(${field.id}, 'required', this.checked)">
                        <label class="form-check-label" for="required-${field.id}">Obligatoire</label>
                    </div>
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-danger btn-sm" onclick="formBuilder.removeField(${field.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="options-container" id="options-${field.id}" style="display: ${field.type === 'select' ? 'block' : 'none'}">
                <label class="form-label">Options</label>
                <div class="input-group mb-2">
                    <input type="text" class="form-control" placeholder="Nouvelle option" id="new-option-${field.id}">
                    <button class="btn btn-outline-secondary" type="button" onclick="formBuilder.addOption(${field.id})">Ajouter</button>
                </div>
                <div id="options-list-${field.id}">
                    ${field.options.map((option, index) => `
                        <div class="input-group mb-1">
                            <input type="text" class="form-control" value="${option}" 
                                   onchange="formBuilder.updateOption(${field.id}, ${index}, this.value)">
                            <button class="btn btn-outline-danger" type="button" onclick="formBuilder.removeOption(${field.id}, ${index})">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        container.appendChild(fieldDiv);
    }

    updateField(fieldId, property, value) {
        const field = this.fields.find(f => f.id === fieldId);
        if (field) {
            field[property] = value;
            
            if (property === 'type') {
                const optionsContainer = document.getElementById(`options-${fieldId}`);
                if (optionsContainer) {
                    optionsContainer.style.display = value === 'select' ? 'block' : 'none';
                }
            }
        }
    }

    removeField(fieldId) {
        this.fields = this.fields.filter(f => f.id !== fieldId);
        document.getElementById(`field-${fieldId}`).remove();
    }

    addOption(fieldId) {
        const field = this.fields.find(f => f.id === fieldId);
        const input = document.getElementById(`new-option-${fieldId}`);
        if (field && input.value.trim()) {
            field.options.push(input.value.trim());
            input.value = '';
            this.renderField(field);
            document.getElementById(`field-${fieldId}`).replaceWith(document.getElementById(`field-${fieldId}`));
        }
    }

    updateOption(fieldId, index, value) {
        const field = this.fields.find(f => f.id === fieldId);
        if (field && field.options[index]) {
            field.options[index] = value;
        }
    }

    removeOption(fieldId, index) {
        const field = this.fields.find(f => f.id === fieldId);
        if (field) {
            field.options.splice(index, 1);
            this.renderField(field);
            document.getElementById(`field-${fieldId}`).replaceWith(document.getElementById(`field-${fieldId}`));
        }
    }

    async saveForm() {
        const formData = {
            name: document.getElementById('formName').value,
            description: document.getElementById('formDescription').value,
            fields: this.fields.map(f => ({
                name: f.name,
                label: f.label,
                type: f.type,
                required: f.required,
                options: f.options
            }))
        };

        try {
            const response = await fetch(`/create_form/${projectId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            if (result.success) {
                showAlert('Formulaire créé avec succès!');
                setTimeout(() => {
                    window.location.href = `/project/${projectId}`;
                }, 1500);
            }
        } catch (error) {
            showAlert('Erreur lors de la création du formulaire', 'error');
        }
    }
}

// Initialisation
let formBuilder;
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('form-builder')) {
        formBuilder = new FormBuilder();
    }
});