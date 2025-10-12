// Global state
let resources = [];
let selectedResource = null;
let draggedElement = null;
let resourceCounter = {
    vpc: 0,
    subnet: 0,
    ec2: 0,
    'security-group': 0
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    initializeDragAndDrop();
    initializeButtons();
});

// Drag and Drop Initialization
function initializeDragAndDrop() {
    const resourceItems = document.querySelectorAll('.resource-item');
    const canvas = document.getElementById('canvas');

    resourceItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragend', handleDragEnd);
    });

    canvas.addEventListener('dragover', handleDragOver);
    canvas.addEventListener('drop', handleDrop);
}

function handleDragStart(e) {
    const resourceType = e.target.closest('.resource-item').dataset.type;
    e.dataTransfer.effectAllowed = 'copy';
    e.dataTransfer.setData('resourceType', resourceType);
}

function handleDragEnd(e) {
    e.target.style.opacity = '1';
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
}

function handleDrop(e) {
    e.preventDefault();
    const resourceType = e.dataTransfer.getData('resourceType');
    
    if (!resourceType) return;

    const canvas = document.getElementById('canvas');
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left + canvas.scrollLeft;
    const y = e.clientY - rect.top + canvas.scrollTop;

    createResource(resourceType, x, y);
}

// Resource Creation
function createResource(type, x, y) {
    resourceCounter[type]++;
    const id = `${type}-${resourceCounter[type]}`;
    
    const resource = {
        id: id,
        type: type,
        x: x,
        y: y,
        properties: getDefaultProperties(type, id)
    };

    resources.push(resource);
    renderResource(resource);
    updateCanvasState();
}

function getDefaultProperties(type, id) {
    const baseName = id;
    
    switch(type) {
        case 'vpc':
            return {
                name: baseName,
                cidr_block: '10.0.0.0/16',
                enable_dns_hostnames: true,
                enable_dns_support: true,
                tags: { Name: baseName }
            };
        case 'subnet':
            return {
                name: baseName,
                vpc_id: '',
                cidr_block: '10.0.1.0/24',
                availability_zone: 'us-east-1a',
                map_public_ip_on_launch: false,
                tags: { Name: baseName }
            };
        case 'ec2':
            return {
                name: baseName,
                ami: 'ami-0c55b159cbfafe1f0',
                instance_type: 't2.micro',
                subnet_id: '',
                vpc_security_group_ids: [],
                tags: { Name: baseName }
            };
        case 'security-group':
            return {
                name: baseName,
                description: 'Security group for ' + baseName,
                vpc_id: '',
                ingress: [
                    {
                        from_port: 22,
                        to_port: 22,
                        protocol: 'tcp',
                        cidr_blocks: ['0.0.0.0/0']
                    }
                ],
                egress: [
                    {
                        from_port: 0,
                        to_port: 0,
                        protocol: '-1',
                        cidr_blocks: ['0.0.0.0/0']
                    }
                ],
                tags: { Name: baseName }
            };
    }
}

// Render Resource on Canvas
function renderResource(resource) {
    const canvas = document.getElementById('canvas');
    const element = document.createElement('div');
    element.className = `dropped-resource ${resource.type}`;
    element.dataset.id = resource.id;
    element.style.left = resource.x + 'px';
    element.style.top = resource.y + 'px';

    const icon = getResourceIcon(resource.type);
    const typeName = getResourceTypeName(resource.type);

    element.innerHTML = `
        <div class="resource-header">
            <div class="resource-title">
                <span>${icon}</span>
                <span>${resource.properties.name}</span>
            </div>
            <button class="delete-btn" onclick="deleteResource('${resource.id}')">×</button>
        </div>
        <div class="resource-info">${typeName}</div>
    `;

    element.addEventListener('click', (e) => {
        e.stopPropagation();
        selectResource(resource.id);
    });

    // Make draggable on canvas
    element.addEventListener('mousedown', startDragging);

    canvas.appendChild(element);
}

function getResourceIcon(type) {
    const icons = {
        vpc: '🌐',
        subnet: '📡',
        ec2: '🖥️',
        'security-group': '🔒'
    };
    return icons[type] || '📦';
}

function getResourceTypeName(type) {
    const names = {
        vpc: 'Virtual Private Cloud',
        subnet: 'Subnet',
        ec2: 'EC2 Instance',
        'security-group': 'Security Group'
    };
    return names[type] || type;
}

// Dragging resources on canvas
let isDragging = false;
let currentDraggedResource = null;
let dragOffsetX = 0;
let dragOffsetY = 0;

function startDragging(e) {
    const element = e.target.closest('.dropped-resource');
    if (!element || e.target.closest('.delete-btn')) return;

    isDragging = true;
    currentDraggedResource = element;
    
    const rect = element.getBoundingClientRect();
    const canvas = document.getElementById('canvas');
    const canvasRect = canvas.getBoundingClientRect();
    
    dragOffsetX = e.clientX - rect.left;
    dragOffsetY = e.clientY - rect.top;

    element.style.cursor = 'grabbing';
    
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDragging);
}

function drag(e) {
    if (!isDragging || !currentDraggedResource) return;
    
    e.preventDefault();
    const canvas = document.getElementById('canvas');
    const rect = canvas.getBoundingClientRect();
    
    let x = e.clientX - rect.left - dragOffsetX + canvas.scrollLeft;
    let y = e.clientY - rect.top - dragOffsetY + canvas.scrollTop;
    
    // Keep within bounds
    x = Math.max(0, x);
    y = Math.max(0, y);
    
    currentDraggedResource.style.left = x + 'px';
    currentDraggedResource.style.top = y + 'px';
}

function stopDragging(e) {
    if (!isDragging) return;
    
    isDragging = false;
    
    if (currentDraggedResource) {
        currentDraggedResource.style.cursor = 'move';
        
        // Update resource position in state
        const id = currentDraggedResource.dataset.id;
        const resource = resources.find(r => r.id === id);
        if (resource) {
            resource.x = parseInt(currentDraggedResource.style.left);
            resource.y = parseInt(currentDraggedResource.style.top);
        }
    }
    
    currentDraggedResource = null;
    
    document.removeEventListener('mousemove', drag);
    document.removeEventListener('mouseup', stopDragging);
}

// Resource Selection
function selectResource(id) {
    // Deselect previous
    document.querySelectorAll('.dropped-resource').forEach(el => {
        el.classList.remove('selected');
    });

    // Select new
    const element = document.querySelector(`[data-id="${id}"]`);
    if (element) {
        element.classList.add('selected');
    }

    selectedResource = resources.find(r => r.id === id);
    renderProperties();
}

// Canvas click to deselect
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    canvas.addEventListener('click', (e) => {
        if (e.target === canvas || e.target.classList.contains('canvas-placeholder')) {
            deselectAll();
        }
    });
});

function deselectAll() {
    document.querySelectorAll('.dropped-resource').forEach(el => {
        el.classList.remove('selected');
    });
    selectedResource = null;
    renderProperties();
}

// Render Properties Panel
function renderProperties() {
    const panel = document.getElementById('propertiesContent');
    
    if (!selectedResource) {
        panel.innerHTML = '<p class="no-selection">Select a resource to edit its properties</p>';
        return;
    }

    let html = '';

    switch(selectedResource.type) {
        case 'vpc':
            html = renderVPCProperties();
            break;
        case 'subnet':
            html = renderSubnetProperties();
            break;
        case 'ec2':
            html = renderEC2Properties();
            break;
        case 'security-group':
            html = renderSecurityGroupProperties();
            break;
    }

    panel.innerHTML = html;
    attachPropertyEventListeners();
}

function renderVPCProperties() {
    const props = selectedResource.properties;
    return `
        <div class="form-group">
            <label>Name</label>
            <input type="text" id="prop-name" value="${props.name}">
        </div>
        <div class="form-group">
            <label>CIDR Block</label>
            <input type="text" id="prop-cidr_block" value="${props.cidr_block}">
        </div>
        <div class="form-group">
            <label>Enable DNS Hostnames</label>
            <select id="prop-enable_dns_hostnames">
                <option value="true" ${props.enable_dns_hostnames ? 'selected' : ''}>True</option>
                <option value="false" ${!props.enable_dns_hostnames ? 'selected' : ''}>False</option>
            </select>
        </div>
        <div class="form-group">
            <label>Enable DNS Support</label>
            <select id="prop-enable_dns_support">
                <option value="true" ${props.enable_dns_support ? 'selected' : ''}>True</option>
                <option value="false" ${!props.enable_dns_support ? 'selected' : ''}>False</option>
            </select>
        </div>
    `;
}

function renderSubnetProperties() {
    const props = selectedResource.properties;
    const vpcs = resources.filter(r => r.type === 'vpc');
    
    return `
        <div class="form-group">
            <label>Name</label>
            <input type="text" id="prop-name" value="${props.name}">
        </div>
        <div class="form-group">
            <label>VPC</label>
            <select id="prop-vpc_id">
                <option value="">Select VPC</option>
                ${vpcs.map(vpc => `
                    <option value="${vpc.id}" ${props.vpc_id === vpc.id ? 'selected' : ''}>
                        ${vpc.properties.name}
                    </option>
                `).join('')}
            </select>
        </div>
        <div class="form-group">
            <label>CIDR Block</label>
            <input type="text" id="prop-cidr_block" value="${props.cidr_block}">
        </div>
        <div class="form-group">
            <label>Availability Zone</label>
            <input type="text" id="prop-availability_zone" value="${props.availability_zone}">
        </div>
        <div class="form-group">
            <label>Map Public IP on Launch</label>
            <select id="prop-map_public_ip_on_launch">
                <option value="true" ${props.map_public_ip_on_launch ? 'selected' : ''}>True</option>
                <option value="false" ${!props.map_public_ip_on_launch ? 'selected' : ''}>False</option>
            </select>
        </div>
    `;
}

function renderEC2Properties() {
    const props = selectedResource.properties;
    const subnets = resources.filter(r => r.type === 'subnet');
    const securityGroups = resources.filter(r => r.type === 'security-group');
    
    return `
        <div class="form-group">
            <label>Name</label>
            <input type="text" id="prop-name" value="${props.name}">
        </div>
        <div class="form-group">
            <label>AMI ID</label>
            <input type="text" id="prop-ami" value="${props.ami}">
        </div>
        <div class="form-group">
            <label>Instance Type</label>
            <select id="prop-instance_type">
                <option value="t2.micro" ${props.instance_type === 't2.micro' ? 'selected' : ''}>t2.micro</option>
                <option value="t2.small" ${props.instance_type === 't2.small' ? 'selected' : ''}>t2.small</option>
                <option value="t2.medium" ${props.instance_type === 't2.medium' ? 'selected' : ''}>t2.medium</option>
                <option value="t3.micro" ${props.instance_type === 't3.micro' ? 'selected' : ''}>t3.micro</option>
                <option value="t3.small" ${props.instance_type === 't3.small' ? 'selected' : ''}>t3.small</option>
            </select>
        </div>
        <div class="form-group">
            <label>Subnet</label>
            <select id="prop-subnet_id">
                <option value="">Select Subnet</option>
                ${subnets.map(subnet => `
                    <option value="${subnet.id}" ${props.subnet_id === subnet.id ? 'selected' : ''}>
                        ${subnet.properties.name}
                    </option>
                `).join('')}
            </select>
        </div>
        <div class="form-group">
            <label>Security Groups</label>
            <div style="max-height: 150px; overflow-y: auto; border: 1px solid #dee2e6; border-radius: 4px; padding: 8px;">
                ${securityGroups.map(sg => `
                    <label style="display: block; margin-bottom: 5px;">
                        <input type="checkbox" class="sg-checkbox" value="${sg.id}" 
                            ${props.vpc_security_group_ids.includes(sg.id) ? 'checked' : ''}>
                        ${sg.properties.name}
                    </label>
                `).join('')}
            </div>
        </div>
    `;
}

function renderSecurityGroupProperties() {
    const props = selectedResource.properties;
    const vpcs = resources.filter(r => r.type === 'vpc');
    
    return `
        <div class="form-group">
            <label>Name</label>
            <input type="text" id="prop-name" value="${props.name}">
        </div>
        <div class="form-group">
            <label>Description</label>
            <input type="text" id="prop-description" value="${props.description}">
        </div>
        <div class="form-group">
            <label>VPC</label>
            <select id="prop-vpc_id">
                <option value="">Select VPC</option>
                ${vpcs.map(vpc => `
                    <option value="${vpc.id}" ${props.vpc_id === vpc.id ? 'selected' : ''}>
                        ${vpc.properties.name}
                    </option>
                `).join('')}
            </select>
        </div>
        <div class="form-group">
            <label>Ingress Rules</label>
            <div class="rules-container" id="ingress-rules">
                ${props.ingress.map((rule, index) => `
                    <div class="rule-item" data-index="${index}">
                        <div style="flex: 1;">
                            Port ${rule.from_port}-${rule.to_port}, ${rule.protocol}, ${rule.cidr_blocks.join(', ')}
                        </div>
                        <button class="remove-rule-btn" onclick="removeIngressRule(${index})">Remove</button>
                    </div>
                `).join('')}
            </div>
            <button class="add-rule-btn" onclick="addIngressRule()">+ Add Ingress Rule</button>
        </div>
        <div class="form-group">
            <label>Egress Rules</label>
            <div class="rules-container" id="egress-rules">
                ${props.egress.map((rule, index) => `
                    <div class="rule-item" data-index="${index}">
                        <div style="flex: 1;">
                            Port ${rule.from_port}-${rule.to_port}, ${rule.protocol}, ${rule.cidr_blocks.join(', ')}
                        </div>
                        <button class="remove-rule-btn" onclick="removeEgressRule(${index})">Remove</button>
                    </div>
                `).join('')}
            </div>
            <button class="add-rule-btn" onclick="addEgressRule()">+ Add Egress Rule</button>
        </div>
    `;
}

// Property Event Listeners
function attachPropertyEventListeners() {
    const inputs = document.querySelectorAll('#propertiesContent input, #propertiesContent select');
    
    inputs.forEach(input => {
        if (input.classList.contains('sg-checkbox')) {
            input.addEventListener('change', handleSecurityGroupCheckbox);
        } else if (input.id.startsWith('prop-')) {
            input.addEventListener('input', handlePropertyChange);
            input.addEventListener('change', handlePropertyChange);
        }
    });
}

function handlePropertyChange(e) {
    if (!selectedResource) return;
    
    const propertyName = e.target.id.replace('prop-', '');
    let value = e.target.value;
    
    // Convert boolean strings
    if (value === 'true') value = true;
    if (value === 'false') value = false;
    
    selectedResource.properties[propertyName] = value;
    
    // Update the visual representation if name changed
    if (propertyName === 'name') {
        const element = document.querySelector(`[data-id="${selectedResource.id}"] .resource-title span:last-child`);
        if (element) {
            element.textContent = value;
        }
    }
}

function handleSecurityGroupCheckbox(e) {
    if (!selectedResource || selectedResource.type !== 'ec2') return;
    
    const sgId = e.target.value;
    const isChecked = e.target.checked;
    
    if (isChecked) {
        if (!selectedResource.properties.vpc_security_group_ids.includes(sgId)) {
            selectedResource.properties.vpc_security_group_ids.push(sgId);
        }
    } else {
        selectedResource.properties.vpc_security_group_ids = 
            selectedResource.properties.vpc_security_group_ids.filter(id => id !== sgId);
    }
}

// Security Group Rule Management
function addIngressRule() {
    if (!selectedResource || selectedResource.type !== 'security-group') return;
    
    const fromPort = prompt('From Port:', '80');
    const toPort = prompt('To Port:', '80');
    const protocol = prompt('Protocol (tcp/udp/icmp/-1):', 'tcp');
    const cidr = prompt('CIDR Block:', '0.0.0.0/0');
    
    if (fromPort && toPort && protocol && cidr) {
        selectedResource.properties.ingress.push({
            from_port: parseInt(fromPort),
            to_port: parseInt(toPort),
            protocol: protocol,
            cidr_blocks: [cidr]
        });
        renderProperties();
    }
}

function removeIngressRule(index) {
    if (!selectedResource || selectedResource.type !== 'security-group') return;
    selectedResource.properties.ingress.splice(index, 1);
    renderProperties();
}

function addEgressRule() {
    if (!selectedResource || selectedResource.type !== 'security-group') return;
    
    const fromPort = prompt('From Port:', '0');
    const toPort = prompt('To Port:', '0');
    const protocol = prompt('Protocol (tcp/udp/icmp/-1):', '-1');
    const cidr = prompt('CIDR Block:', '0.0.0.0/0');
    
    if (fromPort && toPort && protocol && cidr) {
        selectedResource.properties.egress.push({
            from_port: parseInt(fromPort),
            to_port: parseInt(toPort),
            protocol: protocol,
            cidr_blocks: [cidr]
        });
        renderProperties();
    }
}

function removeEgressRule(index) {
    if (!selectedResource || selectedResource.type !== 'security-group') return;
    selectedResource.properties.egress.splice(index, 1);
    renderProperties();
}

// Delete Resource
function deleteResource(id) {
    resources = resources.filter(r => r.id !== id);
    
    const element = document.querySelector(`[data-id="${id}"]`);
    if (element) {
        element.remove();
    }
    
    if (selectedResource && selectedResource.id === id) {
        selectedResource = null;
        renderProperties();
    }
    
    updateCanvasState();
}

// Button Handlers
function initializeButtons() {
    document.getElementById('clearBtn').addEventListener('click', clearCanvas);
    document.getElementById('generateBtn').addEventListener('click', generateTerraform);
    document.getElementById('closeModal').addEventListener('click', closeModal);
    document.getElementById('copyBtn').addEventListener('click', copyTerraformCode);
    document.getElementById('downloadBtn').addEventListener('click', downloadTerraformCode);
}

function clearCanvas() {
    if (resources.length === 0) return;
    
    if (confirm('Are you sure you want to clear all resources?')) {
        resources = [];
        selectedResource = null;
        const canvas = document.getElementById('canvas');
        canvas.querySelectorAll('.dropped-resource').forEach(el => el.remove());
        renderProperties();
        updateCanvasState();
    }
}

function updateCanvasState() {
    const canvas = document.getElementById('canvas');
    if (resources.length > 0) {
        canvas.classList.add('has-items');
    } else {
        canvas.classList.remove('has-items');
    }
}

// Terraform Generation
function generateTerraform() {
    if (resources.length === 0) {
        alert('Please add some resources first!');
        return;
    }

    let terraform = `# Generated by Terraform Visual Builder\n\n`;
    terraform += `terraform {\n  required_version = ">= 1.0"\n  required_providers {\n    aws = {\n      source  = "hashicorp/aws"\n      version = "~> 5.0"\n    }\n  }\n}\n\n`;
    terraform += `provider "aws" {\n  region = "us-east-1"\n}\n\n`;

    // Generate resources in order: VPC -> Subnet -> Security Group -> EC2
    const vpcs = resources.filter(r => r.type === 'vpc');
    const subnets = resources.filter(r => r.type === 'subnet');
    const securityGroups = resources.filter(r => r.type === 'security-group');
    const ec2s = resources.filter(r => r.type === 'ec2');

    vpcs.forEach(resource => {
        terraform += generateVPCTerraform(resource);
    });

    subnets.forEach(resource => {
        terraform += generateSubnetTerraform(resource);
    });

    securityGroups.forEach(resource => {
        terraform += generateSecurityGroupTerraform(resource);
    });

    ec2s.forEach(resource => {
        terraform += generateEC2Terraform(resource);
    });

    // Show in modal
    document.getElementById('terraformCode').textContent = terraform;
    document.getElementById('terraformModal').classList.add('active');
}

function generateVPCTerraform(resource) {
    const props = resource.properties;
    const resourceName = sanitizeName(props.name);
    
    return `resource "aws_vpc" "${resourceName}" {
  cidr_block           = "${props.cidr_block}"
  enable_dns_hostnames = ${props.enable_dns_hostnames}
  enable_dns_support   = ${props.enable_dns_support}

  tags = {
    Name = "${props.name}"
  }
}

`;
}

function generateSubnetTerraform(resource) {
    const props = resource.properties;
    const resourceName = sanitizeName(props.name);
    const vpcRef = props.vpc_id ? `aws_vpc.${sanitizeName(getResourceById(props.vpc_id).properties.name)}.id` : '"REPLACE_WITH_VPC_ID"';
    
    return `resource "aws_subnet" "${resourceName}" {
  vpc_id                  = ${vpcRef}
  cidr_block              = "${props.cidr_block}"
  availability_zone       = "${props.availability_zone}"
  map_public_ip_on_launch = ${props.map_public_ip_on_launch}

  tags = {
    Name = "${props.name}"
  }
}

`;
}

function generateSecurityGroupTerraform(resource) {
    const props = resource.properties;
    const resourceName = sanitizeName(props.name);
    const vpcRef = props.vpc_id ? `aws_vpc.${sanitizeName(getResourceById(props.vpc_id).properties.name)}.id` : '"REPLACE_WITH_VPC_ID"';
    
    let terraform = `resource "aws_security_group" "${resourceName}" {
  name        = "${props.name}"
  description = "${props.description}"
  vpc_id      = ${vpcRef}

`;

    props.ingress.forEach(rule => {
        terraform += `  ingress {
    from_port   = ${rule.from_port}
    to_port     = ${rule.to_port}
    protocol    = "${rule.protocol}"
    cidr_blocks = [${rule.cidr_blocks.map(c => `"${c}"`).join(', ')}]
  }

`;
    });

    props.egress.forEach(rule => {
        terraform += `  egress {
    from_port   = ${rule.from_port}
    to_port     = ${rule.to_port}
    protocol    = "${rule.protocol}"
    cidr_blocks = [${rule.cidr_blocks.map(c => `"${c}"`).join(', ')}]
  }

`;
    });

    terraform += `  tags = {
    Name = "${props.name}"
  }
}

`;

    return terraform;
}

function generateEC2Terraform(resource) {
    const props = resource.properties;
    const resourceName = sanitizeName(props.name);
    const subnetRef = props.subnet_id ? `aws_subnet.${sanitizeName(getResourceById(props.subnet_id).properties.name)}.id` : '"REPLACE_WITH_SUBNET_ID"';
    
    let sgRefs = '[]';
    if (props.vpc_security_group_ids.length > 0) {
        const sgNames = props.vpc_security_group_ids.map(id => {
            const sg = getResourceById(id);
            return sg ? `aws_security_group.${sanitizeName(sg.properties.name)}.id` : '';
        }).filter(Boolean);
        sgRefs = `[${sgNames.join(', ')}]`;
    }
    
    return `resource "aws_instance" "${resourceName}" {
  ami                    = "${props.ami}"
  instance_type          = "${props.instance_type}"
  subnet_id              = ${subnetRef}
  vpc_security_group_ids = ${sgRefs}

  tags = {
    Name = "${props.name}"
  }
}

`;
}

function sanitizeName(name) {
    return name.replace(/[^a-zA-Z0-9_]/g, '_').toLowerCase();
}

function getResourceById(id) {
    return resources.find(r => r.id === id);
}

function closeModal() {
    document.getElementById('terraformModal').classList.remove('active');
}

function copyTerraformCode() {
    const code = document.getElementById('terraformCode').textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert('Terraform code copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function downloadTerraformCode() {
    const code = document.getElementById('terraformCode').textContent;
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'main.tf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

