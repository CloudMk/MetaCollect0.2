// Gestionnaire de formulaires avancé
class AdvancedFormBuilder {
    constructor(projectId) {
        this.projectId = projectId;
        this.fields = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadExistingForms();
    }

    setupEventListeners() {
        // Gestionnaires d'événements pour le builder
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeSortable();
            this.setupFieldTemplates();
        });
    }

    initializeSortable() {
        // Pour le drag & drop des champs
        const container = document.getElementById('fields-container');
        if (container) {
            new Sortable(container, {
                animation: 150,
                ghostClass: 'sortable-ghost',
                onEnd: (evt) => this.updateFieldOrder(evt)
            });
        }
    }

    setupFieldTemplates() {
        // Templates prédéfinis
        const templates = {
            contact: [
                { type: 'text', label: 'Nom complet', required: true },
                { type: 'email', label: 'Email', required: true },
                { type: 'number', label: 'Téléphone', required: false }
            ],
            feedback: [
                { type: 'text', label: 'Nom', required: false },
                { type: 'email', label: 'Email', required: true },
                { type: 'select', label: 'Note de satisfaction', options: ['1', '2', '3', '4', '5'], required: true },
                { type: 'textarea', label: 'Commentaires', required: false }
            ],
            survey: [
                { type: 'text', label: 'Nom', required: true },
                { type: 'number', label: 'Âge', required: true },
                { type: 'select', label: 'Profession', options: ['Étudiant', 'Employé', 'Freelance', 'Autre'], required: true }
            ]
        };

        // Ajouter les boutons de template
        Object.keys(templates).forEach(key => {
            const btn = document.getElementById(`template-${key}`);
            if (btn) {
                btn.addEventListener('click', () => this.loadTemplate(templates[key]));
            }
        });
    }

    loadTemplate(fields) {
        fields.forEach(field => {
            this.addField(field.type, field.label, field.required, field.options || []);
        });
    }

    addField(type = 'text', label = '', required = false, options = []) {
        const field = {
            id: Date.now() + Math.random(),
            type: type,
            name: label.toLowerCase().replace(/\s+/g, '_') || `field_${Date.now()}`,
            label: label,
            required: required,
            options: options,
            validation: this.getDefaultValidation(type)
        };
        
        this.fields.push(field);
        this.renderField(field);
        this.updatePreview();
    }

    getDefaultValidation(type) {
        const validations = {
            text: { min: 1, max: 255 },
            email: { pattern: '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$' },
            number: { min: 0, max: 999999 },
            date: { min: '1900-01-01', max: '2100-12-31' }
        };
        return validations[type] || {};
    }

    renderField(field) {
        const container = document.getElementById('fields-container');
        if (!container) return;

        const fieldDiv = document.createElement('div');
        fieldDiv.className = 'field-item mb-3';
        fieldDiv.dataset.fieldId = field.id;
        
        fieldDiv.innerHTML = this.generateFieldHTML(field);
        container.appendChild(fieldDiv);
        
        // Ajouter les gestionnaires d'événements
        this.attachFieldEvents(fieldDiv, field);
    }

    generateFieldHTML(field) {
        return `
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span class="fw-bold">${field.label || 'Nouveau champ'}</span>
                    <div>
                        <button type="button" class="btn btn-sm btn-outline-secondary me-1" 
                                onclick="formBuilder.duplicateField(${field.id})">
                            <i class="fas fa-copy"></i>
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-danger" 
                                onclick="formBuilder.removeField(${field.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <label class="form-label">Label</label>
                            <input type="text" class="form-control form-label-input" 
                                   value="${field.label}" 
                                   onchange="formBuilder.updateField(${field.id}, 'label', this.value)">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Nom du champ</label>
                            <input type="text" class="form-control form-name-input" 
                                   value="${field.name}" 
                                   onchange="formBuilder.updateField(${field.id}, 'name', this.value)">
                        </div>
                    </div>
                    
                    <div class="row mt-2">
                        <div class="col-md-4">
                            <label class="form-label">Type</label>
                            <select class="form-select form-type-select"
                                    onchange="formBuilder.updateField(${field.id}, 'type', this.value)">
                                <option value="text" ${field.type === 'text' ? 'selected' : ''}>Texte</option>
                                <option value="email" ${field.type === 'email' ? 'selected' : ''}>Email</option>
                                <option value="number" ${field.type === 'number' ? 'selected' : ''}>Nombre</option>
                                <option value="date" ${field.type === 'date' ? 'selected' : ''}>Date</option>
                                <option value="textarea" ${field.type === 'textarea' ? 'selected' : ''}>Texte long</option>
                                <option value="select" ${field.type === 'select' ? 'selected' : ''}>Liste</option>
                                <option value="checkbox" ${field.type === 'checkbox' ? 'selected' : ''}>Case à cocher</option>
                                <option value="radio" ${field.type === 'radio' ? 'selected' : ''}>Bouton radio</option>
                            </select>
                        </div>
                        <div class="col-md-4">
                            <div class="form-check mt-4">
                                <input class="form-check-input" type="checkbox" 
                                       ${field.required ? 'checked' : ''}
                                       onchange="formBuilder.updateField(${field.id}, 'required', this.checked)">
                                <label class="form-check-label">Obligatoire</label>
                            </div>
                        </div>
                    </div>

                    ${this.getOptionsHTML(field)}
                    ${this.getValidationHTML(field)}
                </div>
            </div>
        `;
    }

    getOptionsHTML(field) {
        if (['select', 'checkbox', 'radio'].includes(field.type)) {
            return `
                <div class="mt-3">
                    <label class="form-label">Options</label>
                    <div class="options-container">
                        ${field.options.map((opt, idx) => `
                            <div class="input-group mb-2">
                                <input type="text" class="form-control" value="${opt}" 
                                       onchange="formBuilder.updateOption(${field.id}, ${idx}, this.value)">
                                <button class="btn btn-outline-danger" type="button" 
                                        onclick="formBuilder.removeOption(${field.id}, ${idx})">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                        `).join('')}
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-primary" 
                            onclick="formBuilder.addOption(${field.id})">
                        <i class="fas fa-plus"></i> Ajouter option
                    </button>
                </div>
            `;
        }
        return '';
    }

    getValidationHTML(field) {
        return `
            <div class="mt-3">
                <label class="form-label">Validation</label>
                <div class="row">
                    <div class="col-md-6">
                        <input type="text" class="form-control" placeholder="Placeholder"
                               value="${field.placeholder || ''}"
                               onchange="formBuilder.updateField(${field.id}, 'placeholder', this.value)">
                    </div>
                    <div class="col-md-6">
                        <input type="text" class="form-control" placeholder="Message d'erreur"
                               value="${field.error_message || ''}"
                               onchange="formBuilder.updateField(${field.id}, 'error_message', this.value)">
                    </div>
                </div>
            </div>
        `;
    }

    duplicateField(fieldId) {
        const field = this.fields.find(f => f.id === fieldId);
        if (field) {
            const newField = { ...field, id: Date.now() + Math.random() };
            this.fields.push(newField);
            this.renderField(newField);
        }
    }

    async saveForm() {
        const formName = document.getElementById('formName').value;
        const formDescription = document.getElementById('formDescription').value;

        if (!formName.trim()) {
            alert('Veuillez entrer un nom pour le formulaire');
            return;
        }

        if (this.fields.length === 0) {
            alert('Veuillez ajouter au moins un champ');
            return;
        }

        const formData = {
            name: formName,
            description: formDescription,
            fields: this.fields.map(f => ({
                name: f.name,
                label: f.label,
                type: f.type,
                required: f.required,
                options: f.options,
                placeholder: f.placeholder,
                error_message: f.error_message
            }))
        };

        try {
            const response = await fetch(`/forms/create/${this.projectId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();
            if (result.success) {
                this.showNotification('Formulaire créé avec succès!', 'success');
                setTimeout(() => {
                    window.location.href = `/projects/${this.projectId}`;
                }, 1500);
            }
        } catch (error) {
            this.showNotification('Erreur lors de la création', 'error');
        }
    }

    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
}

// Initialisation globale
window.FormBuilder = AdvancedFormBuilder;