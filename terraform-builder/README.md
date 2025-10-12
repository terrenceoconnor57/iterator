# 🏗️ Terraform Visual Builder

A modern drag-and-drop web application for visually designing AWS infrastructure and generating Terraform code.

## Features

- **Visual Design**: Drag and drop AWS resources onto a canvas
- **Supported Resources**:
  - VPC (Virtual Private Cloud)
  - Subnets
  - EC2 Instances
  - Security Groups
- **Property Configuration**: Edit resource properties through an intuitive properties panel
- **Terraform Generation**: Generate production-ready Terraform code from your visual design
- **Export Options**: Copy to clipboard or download as `main.tf`

## Getting Started

1. Open `index.html` in a modern web browser
2. Drag resources from the left palette onto the canvas
3. Click on resources to select them and edit their properties in the right panel
4. Configure relationships (e.g., assign subnets to VPCs, security groups to EC2 instances)
5. Click "Generate Terraform" to see your infrastructure as code

## How to Use

### Adding Resources

1. Find the resource you want in the left **Resources** panel
2. Drag it onto the canvas in the center
3. The resource will appear with default properties

### Configuring Resources

1. Click on any resource on the canvas to select it
2. The **Properties** panel on the right will show editable fields
3. Configure properties like:
   - Names and CIDR blocks
   - VPC assignments for subnets and security groups
   - AMI IDs and instance types for EC2
   - Security group rules (ingress/egress)

### Organizing Resources

- Drag resources around the canvas to organize your infrastructure visually
- Delete resources using the × button on each resource
- Clear the entire canvas with the "Clear All" button

### Generating Terraform

1. Click the **Generate Terraform** button
2. Review the generated Terraform code in the modal
3. Either:
   - Copy to clipboard
   - Download as `main.tf` file

## Resource Relationships

The application handles resource dependencies automatically:

- **Subnets** reference VPCs via dropdown selection
- **EC2 instances** can be assigned to subnets and multiple security groups
- **Security Groups** must be assigned to a VPC

The generated Terraform code uses proper resource references (e.g., `aws_vpc.main.id`) instead of hardcoded IDs.

## Example Workflow

1. Drag a **VPC** onto the canvas
2. Configure its CIDR block (e.g., `10.0.0.0/16`)
3. Drag a **Subnet** onto the canvas
4. Select the subnet and assign it to your VPC
5. Configure the subnet's CIDR (e.g., `10.0.1.0/24`)
6. Drag a **Security Group** onto the canvas
7. Assign it to the VPC and configure ingress/egress rules
8. Drag an **EC2 Instance** onto the canvas
9. Configure its AMI, instance type, subnet, and security groups
10. Click **Generate Terraform** to see the complete infrastructure code

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

Requires a modern browser with support for:
- Drag and Drop API
- ES6 JavaScript
- CSS Grid

## Technical Details

- Pure HTML/CSS/JavaScript (no frameworks required)
- No backend server needed
- All processing happens in the browser
- Generated Terraform uses AWS Provider v5.0+
- Terraform version requirement: >= 1.0

## Tips

- Use descriptive names for resources to make the generated Terraform more readable
- The visual layout on the canvas is for organization only - it doesn't affect the generated code
- You can drag VPCs and subnets to create visual hierarchies, though nesting isn't enforced
- Always configure VPCs before creating subnets and security groups
- Check that all resource references are properly set before generating Terraform

## Limitations

This is an example/demonstration application with some limitations:

- Only supports 4 AWS resource types (VPC, Subnet, EC2, Security Group)
- No validation of CIDR block conflicts
- No visual connection lines between related resources
- Security group rules are added via prompts (not inline forms)
- Generated code assumes us-east-1 region (can be changed in the generated code)
- No state management or project saving/loading

## Future Enhancements

Potential improvements could include:

- More AWS resources (RDS, ELB, S3, etc.)
- Visual connection lines showing resource relationships
- CIDR block validation and conflict detection
- Save/load project functionality
- Export to other IaC tools (CloudFormation, Pulumi, etc.)
- Multi-region support
- Visual nesting of resources within VPCs/subnets
- Inline form for security group rules
- Resource templates and presets

## License

This is a demonstration project. Feel free to use and modify as needed.

