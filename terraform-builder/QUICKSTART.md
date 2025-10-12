# Quick Start Guide

## Get Started in 30 Seconds

1. **Open the application**
   ```bash
   # Navigate to the terraform-builder directory
   cd terraform-builder
   
   # Open index.html in your browser
   # On Mac:
   open index.html
   # On Linux:
   xdg-open index.html
   # On Windows:
   start index.html
   ```

2. **Build your first infrastructure**
   - Drag a **VPC** from the left panel onto the canvas
   - Drag a **Subnet** onto the canvas
   - Click the subnet and select the VPC from the dropdown
   - Drag an **EC2 Instance** onto the canvas
   - Click the EC2 and assign it to the subnet
   - Click **Generate Terraform**

3. **Get your code**
   - Click "Copy to Clipboard" or "Download main.tf"
   - Use the generated code in your Terraform projects

## Example: Simple Web Server Setup

Follow these steps to create a basic web server infrastructure:

### Step 1: Create VPC
- Drag VPC to canvas
- Click it and set:
  - Name: `main-vpc`
  - CIDR: `10.0.0.0/16`

### Step 2: Create Subnet
- Drag Subnet to canvas
- Click it and set:
  - Name: `public-subnet`
  - VPC: `main-vpc`
  - CIDR: `10.0.1.0/24`
  - Map Public IP: `True`

### Step 3: Create Security Group
- Drag Security Group to canvas
- Click it and set:
  - Name: `web-sg`
  - VPC: `main-vpc`
  - Description: `Security group for web server`
- Add ingress rules:
  - Port 80 (HTTP)
  - Port 443 (HTTPS)
  - Port 22 (SSH)

### Step 4: Create EC2 Instance
- Drag EC2 to canvas
- Click it and set:
  - Name: `web-server`
  - Instance Type: `t2.micro`
  - Subnet: `public-subnet`
  - Security Groups: Check `web-sg`

### Step 5: Generate
- Click **Generate Terraform**
- See your complete infrastructure as code!

## Keyboard Shortcuts

- **Click**: Select a resource
- **Drag**: Move resources around
- **Delete button** (×): Remove a resource
- **Esc** or click canvas: Deselect all

## Tips

✅ **Do:**
- Create VPCs before subnets
- Use descriptive names
- Configure all relationships
- Review generated code before use

❌ **Don't:**
- Forget to assign subnets to VPCs
- Use overlapping CIDR blocks
- Leave required fields empty

## Troubleshooting

**Q: Resources won't drag?**  
A: Make sure you're dragging from the palette, not the canvas resources.

**Q: Can't select a resource?**  
A: Click directly on the resource card, not empty canvas space.

**Q: Properties panel is empty?**  
A: Click a resource on the canvas to view/edit its properties.

**Q: Generated code has "REPLACE_WITH_VPC_ID"?**  
A: You forgot to assign the subnet/security group to a VPC. Select it and choose a VPC from the dropdown.

## What's Next?

- Customize the generated Terraform code
- Add additional resources manually
- Use terraform plan and apply
- Extend this tool with more AWS resources

Enjoy building! 🚀

